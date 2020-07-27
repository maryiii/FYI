# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 05:59:35 2020

@author: hardi
"""

import os
import numpy as np
import jpype
import pickle
import multiprocessing as mp
from itertools import product
import sys

jarLocation = os.path.join(os.getcwd(),"infodynamics.jar")
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
if not jpype.isJVMStarted():
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea","-Xmx4096m", "-Djava.class.path=" + jarLocation)


def load_data(session):
    datafolder = 'F:/Steinmetz_Data/Spike_times/'
    datafile = f"dat_st_{session}.pkl"
    datapath = os.path.join(datafolder,datafile)
    
    with open(datapath,'rb') as f:
        data = pickle.load(f)
    
    return data

def get_mean_spks(spks):
    neurons,trials = np.shape(spks)
    num_spks = np.zeros((neurons,trials))
    for i in range(neurons):
        for j in range(trials):
            num_spks[i,j] = len(spks[i,j])
    mean_spks = np.mean(num_spks,axis=1)
    return mean_spks


def convert_to_train(ts,bin_size=0.002):
    tbins = int(2/bin_size)
    trials = len(ts)
    strain = np.zeros((trials,tbins),dtype=np.int8)
    for i in range(trials):
        if(len(ts[i])>0):
            if(np.sum(ts[i]<0)):
                print("Negative Time Stamps!")
            stamps = ((ts[i])/bin_size).astype(int)
            stamps = stamps[stamps<tbins]
            strain[i][stamps] = np.ones_like(stamps)
    return strain

def get_te_parallel(p1,p2,n1t,n2t,bin_size,resp_times,k,tau_max):
    print(f"({p1},{p2})",end='...')
    sys.stdout.flush()
    te_calc = jpype.JPackage("infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete
    n1 = convert_to_train(n1t,bin_size)
    n2 = convert_to_train(n2t,bin_size)
    trials = np.shape(n1)[0]
    n1[n1>1] = 1
    n2[n2>1] = 1
    base = 2
    te = 0
    delay = 1
    pv = 1
    for tau in range(1,tau_max+1,1):
        tec = te_calc(base,k,k)
        tec.initialise()
        for j in range(trials):
            src = n1[j,:resp_times[j]-tau]
            trg = n2[j,tau:resp_times[j]]
            tec.addObservations(src.tolist(),trg.tolist())
        te_temp = tec.computeAverageLocalOfObservations()
        surr_dist = tec.computeSignificance(100)
        te_net = te_temp - surr_dist.getMeanOfDistribution()
        pval = surr_dist.pValue
        del tec
        if(te_net<0):
            te_net = 0
        if(te_temp>=te):
            te = te_temp
            delay = tau
            pv = pval
        else:
            break
    return [(p1,p2),(te, delay, pv)]

def get_net_parallel(spks,resp_stamp,bin_size):
    neurons,_ = np.shape(spks) 
    print(f"Number of Neurons: {neurons}")
    pairs = product(np.arange(neurons),np.arange(neurons))
    pairs = [p for p in pairs if p[0]!=p[1]]
    arglist = [(p[0], p[1], spks[p[0]], spks[p[1]], bin_size, resp_stamp, 5, 20) for p in pairs]
    process_pool = mp.Pool(10)
    results = process_pool.starmap_async(get_te_parallel,arglist,chunksize=len(pairs)//10).get()
    process_pool.close()
    
    net = np.zeros((neurons,neurons,3))    
    for i,result in enumerate(results):
        src = result[0][0]
        trg = result[0][1]
        net[src,trg] = result[1]
        
    return net

    

if(__name__=="__main__"):
    session = 3#int(sys.argv[1])-1#3
    bin_size = 0.002
    print(f"Loading Data for session {session}")
    data = load_data(session)
    beh_data = np.load('alldat_beh.npy',allow_pickle=True)
    beh_data = beh_data[session]
    
    print("Curating the data")
    spks = data['ss']
    
    mean_spks = get_mean_spks(spks)
    br = beh_data['brain_area']
    #spks = spks[mean_spks>10]
    #br = br[mean_spks>10]
    
    resp_time = beh_data['response_time']
    resp_stamp = (resp_time/bin_size).astype(int).squeeze()
    feedback =  beh_data['feedback_type']
    c_right = beh_data['contrast_right']
    c_left = beh_data['contrast_left']
    pos_trials = np.logical_and(feedback==1,c_right!=c_left)
    neg_trials = np.logical_and(feedback==-1,c_right!=c_left)
    unc_trials = c_right==c_left
    
    pos_spks = spks[:,pos_trials]
    pos_resp_stamp = resp_stamp[pos_trials]
    neg_spks = spks[:,neg_trials]
    neg_resp_stamp = resp_stamp[neg_trials]
    unc_spks = spks[:,unc_trials]
    unc_resp_stamp = resp_stamp[unc_trials]
    
    pass_spks = data['ss_passive']
    mean_pass_spks = get_mean_spks(pass_spks)
    #pass_spks = pass_spks[mean_pass_spks>10]
    #br_pass = beh_data['brain_area'][mean_pass_spks>10]
    
    pass_trials = np.shape(pass_spks)[1]
    pass_resp_stamp = (np.mean(resp_stamp)*np.ones(pass_trials)).astype(int)
    
    '''
    
    print("Estimating the network for correct trials")
    pos_net = get_net_parallel(pos_spks,pos_resp_stamp,bin_size)
    print("Estimating the network for incorrect trials")
    neg_net = get_net_parallel(neg_spks,neg_resp_stamp,bin_size)
    print("Estimating the network for uncertain trials")
    unc_net = get_net_parallel(unc_spks,unc_resp_stamp,bin_size)
    print("Estimating the network for passive trials")
    pass_net = get_net_parallel(pass_spks,pass_resp_stamp,bin_size)
    
    print("Combining Results")
    results = {'Correct Network':pos_net,'Correct Brain Areas':br,
               'Incorrect Network':neg_net,'Incorrect Brain Areas':br,
               'Uncertain Network':unc_net,'Uncertain Brain Areas':br,
               'Passive Network':pass_net, 'Passive Brain Areas':br_pass}
    
    print("Saving Results")
    savefolder = 'Networks'
    savename = f"NetResults_{session}.pkl"
    savepath = os.path.join(savefolder,savename)
    with open(savepath,"wb") as f:
        pickle.dump(results,f)
    
    '''