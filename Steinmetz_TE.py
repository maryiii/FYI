# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 05:59:35 2020

@author: hardi
"""

import os
import numpy as np
import jpype
import pickle


def get_brain_groupings():
    regions = ["vis ctx", "thal", "hipp", "other ctx", "midbrain", "basal ganglia", "cortical subplate", "other"]
    brain_groups = [["VISa", "VISam", "VISl", "VISp", "VISpm", "VISrl"], # visual cortex
                    ["CL", "LD", "LGd", "LH", "LP", "MD", "MG", "PO", "POL", "PT", "RT", "SPF", "TH", "VAL", "VPL", "VPM"], # thalamus
                    ["CA", "CA1", "CA2", "CA3", "DG", "SUB", "POST"], # hippocampal
                    ["ACA", "AUD", "COA", "DP", "ILA", "MOp", "MOs", "OLF", "ORB", "ORBm", "PIR", "PL", "SSp", "SSs", "RSP"," TT"], # non-visual cortex
                    ["APN", "IC", "MB", "MRN", "NB", "PAG", "RN", "SCs", "SCm", "SCig", "SCsg", "ZI"], # midbrain
                    ["ACB", "CP", "GPe", "LS", "LSc", "LSr", "MS", "OT", "SNr", "SI"], # basal ganglia 
                    ["BLA", "BMA", "EP", "EPd", "MEA"] # cortical subplate
                    ]
    groupings = dict(zip(regions,brain_groups))
    return regions, groupings

jarLocation = os.path.join(os.getcwd(),"infodynamics.jar")
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
if not jpype.isJVMStarted():
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea","-Xmx4096m", "-Djava.class.path=" + jarLocation)


def load_data(folder_name="Preprocessed_Data"):
    datafolder = os.path.join(os.getcwd(),folder_name)
    datafiles = os.listdir(datafolder)
    
    for i,file in enumerate(datafiles):
        datapath = os.path.join(datafolder,file)
        if(i==0):
            alldat = np.load(datapath, allow_pickle=True)['dat']
        else:
            alldat = np.hstack((alldat, np.load(datapath, allow_pickle=True)['dat']))
    
    return alldat

def discretize(a):
    da = np.zeros_like(a)
    for j in range(len(a)):
        uqs = np.unique(a[j])
        nsm = len(uqs)
        dic = dict(zip(uqs,np.arange(nsm).astype(int)))
        disc = np.array([dic[i] for i in a[j]]).astype(int)
        da[j] = disc
    return da

def get_te(n1,n2,resp_times,k,tau_max):
    te_calc = jpype.JPackage("infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete
    trials = np.shape(n1)[0]
    dn1 = discretize(n1)
    dn2 = discretize(n2)
    base = max([np.max(dn1),np.max(dn2)])+1
    te = 0
    delay = 1
    pv = 1
    for tau in range(1,tau_max+1,1):
        tec = te_calc(base,k,k)
        tec.initialise()
        for j in range(trials):
            src = dn1[j,:resp_times[j]-tau]
            trg = dn2[j,tau:resp_times[j]]
            tec.addObservations(src.tolist(),trg.tolist())
        te_temp = tec.computeAverageLocalOfObservations()
        surr_dist = tec.computeSignificance(100)
        te_net = te_temp - surr_dist.getMeanOfDistribution()
        pval = surr_dist.pValue
        if(te_net<0):
            te_net = 0
        if(te_temp>=te):
            te = te_temp
            delay = tau
            pv = pval
        else:
            break
    return te, delay, pv


def get_sess_area_dist(alldata):
    regions, groupings = get_brain_groupings()
    sessions = len(alldata)
    num_areas = []
    for session in range(sessions):
        br = alldata[session]['brain_area']
        nums = []
        for region in regions:
            nums.append(np.sum(np.isin(br,groupings[region])))
        num_areas.append(nums)
    return num_areas

def get_net(spks,resp_stamp):
    neurons,_,_ =np.shape(spks) 
    net = np.zeros((neurons,neurons,3))    
    for i in range(neurons):
        print(i)
        for j in range(neurons):
            print(j,end='...')
            if(i!=j):
                net[i,j] = get_te(spks[i],spks[j],resp_stamp,3,10)
    print("\n")
    return net

    

if(__name__=="__main__"):
    session = 3
    print(f"Loading Data for session {session}")
    alldata = load_data()
    
    print("Curating the data")
    data = alldata[session]
    spks = data['spks']
    mean_spks = np.mean(spks,axis=(1,2))
    br = data['brain_area']
    spks = spks[mean_spks>0.05]
    br = br[mean_spks>0.05]
    
    
    resp_time = data['response_time']
    resp_stamp = (100*resp_time).astype(int).squeeze()
    feedback = data['feedback_type']
    
    pos_spks = spks[:,feedback==1,50:]
    pos_resp_stamp = resp_stamp[feedback==1]
    neg_spks = spks[:,feedback==-1,50:]
    neg_resp_stamp = resp_stamp[feedback==-1]
    
    pass_spks = data['spks_passive'][:,:,50:]
    mean_pass_spks = np.mean(pass_spks,axis=(1,2))
    pass_spks = pass_spks[mean_pass_spks>0.05]
    br_pass = data['brain_area'][mean_pass_spks>0.05]
    pass_trials = np.shape(pass_spks)[1]
    pass_resp_stamp = 200*np.ones(pass_trials).astype(int)
    
    print("Estimating the network for correct trials")
    pos_net = get_net(pos_spks,pos_resp_stamp)
    print("Estimating the network for incorrect trials")
    neg_net = get_net(neg_spks,neg_resp_stamp)
    print("Estimating the network for passive trials")
    pass_net = get_net(pass_spks,pass_resp_stamp)
    
    print("Combining Results")
    results = {'Correct Network':pos_net,'Correct Brain Areas':br,
               'Incorrect Network':neg_net,'Incorrect Brain Areas':br,
               'Passive Network':pass_net, 'Passive Brain Areas':br_pass}
    
    print("Saving Results")
    with open(f"NetResults_{session}.pkl","wb") as f:
        pickle.dump(results,f)
