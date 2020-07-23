# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 05:59:35 2020

@author: hardi
"""

import os, requests
import numpy as np
import jpype
#from idtxl.multivariate_te import MultivariateTE
#from idtxl.data import Data


jarLocation = os.path.join(os.getcwd(),"infodynamics.jar")
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
if not jpype.isJVMStarted():
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea","-Xmx4096m", "-Djava.class.path=" + jarLocation)


def load_data(mouse_no, folder_name="Preprocessed_Data"):
    datafolder = os.path.join(os.getcwd(),folder_name)
    datafiles = os.listdir(datafolder)
    
    for i,file in enumerate(datafiles):
        datapath = os.path.join(datafolder,file)
        if(i==0):
            alldat = np.load(datapath, allow_pickle=True)['dat']
        else:
            alldat = np.hstack((alldat, np.load(datapath, allow_pickle=True)['dat']))
    dat = alldat[mouse_no]
    return dat

'''
def Net_Gen(data,tau_max):
    neurons, trials, T = np.shape(data)
    settings = {'cmi_estimator': 'JidtDiscreteCMI',#Discrete for spike trains use JidtGaussianCMI for continuous
                'max_lag_sources': tau_max,
                'min_lag_sources': 1,
                'n_discrete_bins': np.max(data)+1,
                'permute_in_time': True}#Should be 2 for binary spike trains
     
    mte = MultivariateTE()
    d = Data(data,'prs',normalise=False)#For neurons * trials * timesteps format Normalize = False for spike trains
    results = mte.analyse_network(settings=settings, data = d)
    net = np.zeros((neurons,neurons))
    for i in range(neurons):
        r_dict = results.get_single_target(i,False)
        svs = r_dict['selected_vars_sources']#Find sources for the target
        tes = r_dict['te']#Find TE values for the corresponding sources
        srcs = []
        for s in svs:
            if s[0] not in srcs:
                srcs.append(s[0])#To get rid of multiple lags from same source
        for k,j in enumerate(srcs):
            net[j,i] = tes[k]
    return net
'''
def discretize(a):
    da = np.zeros_like(a)
    for j in range(len(a)):
        a[j] = a[j].astype(int)
        uqs = np.unique(a[j])
        nsm = len(uqs)
        dic = dict(zip(uqs,np.arange(nsm).astype(int)))
        disc = np.array([dic[i] for i in a]).astype(int)
        da[j] = disc
    return disc

def get_te(n1,n2,resp_times,k,tau_max):
    te_calc = jpype.JPackage("infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete
    trials = np.shape(n1)[0]
    dn1 = discretize(n1)
    dn2 = discretize(n2)
    base = max([np.max(dn1),np.max(dn2)])+1
    te = 0
    delay = 1
    for tau in range(1,tau_max+1,1):
        tec = te_calc(base,k,k)
        tec.initialise()
        for j in range(trials):
            #da,ba = discretize(n1[j])
            #db,bb = discretize(n2[j])
            src = dn1[j,:resp_times[j]-tau]
            trg = dn2[j,tau:resp_times[j]]
            tec.addObservations(src.tolist(),trg.tolist())
        te_temp = tec.computeAverageLocalOfObservations()
        if(te_temp>te):
            te = te_temp
            delay = tau
        else:
            break
    return te, delay


    


print("Loading Data")
data = load_data(11)
spks = data['spks']
resp_time = data['response_time']
resp_stamp = (100*resp_time).astype(int).squeeze()
feedback = data['feedback_type']
pos_spks = spks[:,feedback==1,50:]
pos_resp_stamp = resp_stamp[feedback==1]
neg_spks = spks[:,feedback==-1,50:]
neg_resp_stamp = resp_stamp[feedback==-1]
pass_spks = data['spks_passive'][:,:,50:]

neurons,_,_ =np.shape(spks)
 
net = np.zeros((neurons,neurons))

for i in range(neurons):
    print(i)
    for j in range(neurons):
        if(i!=j):
            net[i,j],_ = get_te(pos_spks[i],pos_spks[j],pos_resp_stamp,3,10)

#print("Getting the Network")
#net = Net_Gen(data,5)