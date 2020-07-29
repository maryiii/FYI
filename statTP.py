#import matplotlib.pylab as plt
#from networkx.algorithms.community import greedy_modularity_communities
#from networkx.algorithms.community import asyn_lpa_communities
import pickle
import scipy.stats as stats
from statsmodels.stats import multitest
import numpy as np
#import community as community_louvain
#from networkx.algorithms.community import asyn_lpa_communities

#read the input data from .pkl file into a dictionary
def pickle_reader(file):
    with open(file, 'rb') as handle:
        whole_data = pickle.load(handle)
    
    return whole_data


def ttest_calc(edge_data, edge_data1):
    final_stats = dict()
    for key in edge_data.keys():
        if key in edge_data1.keys():
            list_1 = edge_data[key]
            list_2 = edge_data1[key]
            if list_1 == list_2:
                continue
            t, p = stats.ttest_ind(list_1, list_2, equal_var = False)
            final_stats[key] = [t, p]
            
    return final_stats

def anova_test(edge_data, edge_data1, edge_data2):
    final_stats = dict()
    for key in edge_data.keys():
        if key in edge_data1.keys() and key in edge_data2.keys():
            list_1 = edge_data[key]
            list_2 = edge_data1[key]
            list_3 = edge_data2[key]
            f, p = stats.f_oneway(list_1, list_2, list_3)
            final_stats[key] = [f, p]
            
def combine_active(edge_data, edge_data1, edge_data2):
    final_combined_edges = dict()
    final_combined_edges.update(edge_data)
    for key in edge_data1.keys():
        list_edges = edge_data1[key]
        #(list_edges)
        if key in final_combined_edges.keys():
            final_combined_edges[key].extend(list_edges)
        else:
            final_combined_edges[key] = list_edges   

    for key in edge_data2.keys():
        list_edges = edge_data2[key]
        if key in final_combined_edges.keys():
            final_combined_edges[key].extend(list_edges)
        else:
            final_combined_edges[key] = list_edges 
    #print(final_combined_edges)        
    return final_combined_edges


def find_significant_vals(final_stats):
    significant_vals = dict()
    for key in final_stats.keys():
        t = final_stats[key][0]
        p = final_stats[key][1]
        if p < 0.05:
            significant_vals[key] = t
                        
    return significant_vals

'''
def FDR_correction(whole_p_vals):
    list_of_p_vals = []
    idx = 0
    dict_of_keys = dict()
    for key in whole_p_vals.keys():
        #print(key)
        if not np.isnan(whole_p_vals[key][1]):
            list_of_p_vals.append(whole_p_vals[key][1])
        dict_of_keys[idx] = key
        idx += 1
    print(list_of_p_vals)
    #print(dict_of_keys)
    is_correct, p_val = multitest.fdrcorrection(list_of_p_vals, alpha=0.05)
    print(is_correct)
    
    for i in range(idx):
        real_dict_key = dict_of_keys[i]
        if is_correct[i] == False:
            whole_p_vals.pop(real_dict_key)
        else:
            whole_p_vals[real_dict_key][1] = list_of_p_vals[i] 
        
    return whole_p_vals
'''

def write_dict(name, dict_of_final_edges):
    f = open(name, 'wb')
    pickle.dump(dict_of_final_edges, f)
    f.close()



edge_data_correct = pickle_reader('outputs/correct_net.pkl')
edge_data_incorrect = pickle_reader('outputs/incorrect_net.pkl')
edge_data_passive = pickle_reader('outputs/passive_net.pkl')
edge_data_uncertain = pickle_reader('outputs/uncertain_net.pkl')
ttest_vals_ci = ttest_calc(edge_data_correct, edge_data_incorrect)
#final_p = FDR_correction(ttest_vals_ci)
#print(final_p)
final_sig_vals_ci= find_significant_vals(ttest_vals_ci)
ttest_vals_cp = ttest_calc(edge_data_correct, edge_data_passive)
final_sig_vals_cp = find_significant_vals(ttest_vals_cp)
ttest_vals_ip = ttest_calc(edge_data_incorrect, edge_data_passive)
final_sig_vals_ip = find_significant_vals(ttest_vals_ip)
ttest_vals_up = ttest_calc(edge_data_uncertain, edge_data_passive)
final_sig_vals_up = find_significant_vals(ttest_vals_up)
ttest_vals_ui = ttest_calc(edge_data_uncertain, edge_data_incorrect)
final_sig_vals_ui = find_significant_vals(ttest_vals_ui)
ttest_vals_uc = ttest_calc(edge_data_uncertain, edge_data_correct)
final_sig_vals_uc = find_significant_vals(ttest_vals_uc)
combined_active = combine_active(edge_data_correct, edge_data_incorrect, edge_data_uncertain)
combined_certain = combine_active(edge_data_correct, edge_data_incorrect, dict())
ttest_vals_ap = ttest_calc(combined_active, edge_data_passive)
final_sig_vals_ap = find_significant_vals(ttest_vals_ap)
ttest_vals_ceu = ttest_calc(combined_certain, edge_data_uncertain)
final_sig_vals_ceu = find_significant_vals(ttest_vals_ceu)
#print(final_sig_vals_uc)
write_dict('statistical_results/correctIncorrect.pkl', final_sig_vals_ci)
write_dict('statistical_results/correctPassive.pkl', final_sig_vals_cp)
write_dict('statistical_results/incorrectPassive.pkl', final_sig_vals_ip)
write_dict('statistical_results/correctUncertain.pkl', final_sig_vals_uc)
write_dict('statistical_results/incorrectuncertain.pkl', final_sig_vals_ui)
write_dict('statistical_results/passiveUncertain.pkl', final_sig_vals_up)
write_dict('statistical_results/activePassive.pkl', final_sig_vals_ap)
write_dict('statistical_results/certainUncertain.pkl', final_sig_vals_ceu)
