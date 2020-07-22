# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 05:59:35 2020

@author: hardi
"""

import os, requests
import numpy as np
import jpype
from idtxl.multivariate_te import MultivariateTE
from idtxl.data import Data

'''
jarLocation = os.path.join(os.getcwd(),"infodynamics.jar")
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
if not jpype.isJVMStarted():
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea","-Xmx1024m", "-Djava.class.path=" + jarLocation)
'''

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


def Net_Gen(data,tau_max):
    neurons, trials, T = np.shape(data)
    settings = {'cmi_estimator': 'JidtDiscreteCMI',#Discrete for spike trains use JidtGaussianCMI for continuous
                'max_lag_sources': tau_max,
                'min_lag_sources': 1,
                'n_discrete_bins': np.max(data)+1}#Should be 2 for binary spike trains
     
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

print("Loading Data")
data = load_data(11)
print("Getting the Network")
net = Net_Gen(data,5)