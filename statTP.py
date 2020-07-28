#import matplotlib.pylab as plt
#from networkx.algorithms.community import greedy_modularity_communities
#from networkx.algorithms.community import asyn_lpa_communities
import pickle
import scipy.stats as stats
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
            t, p =stats.ttest_ind(list_1, list_2, equal_var = False)
            final_stats[key] = [t, p]
            
    return final_stats

def anova_test(edge_data, edge_data1, edge_data2):
    final_stats = dict()
    for key in edge_data.keys():
        if key in edge_data1.keys() && key in edge_data2.keys():
            list_1 = edge_data[key]
            list_2 = edge_data1[key]
            list_3 = edge_data2[key]
            f, p = stats.f_oneway(list_1, list_2, list_3)
            final_stats[key] = [f, p]


def find_significant_vals(final_stats):
    significant_vals = dict()
    sumi = 0
    for key in final_stats.keys():
        p = final_stats[key][1]
        if p < 0.05:
            significant_vals[key] = p
            sumi += 1
            
    print(sumi)
    return significant_vals


def write_dict(name, dict_of_final_edges):
    f = open(name, 'wb')
    pickle.dump(dict_of_final_edges, f)
    f.close()



edge_data_correct = pickle_reader('outputs/correct_net.pkl')
edge_data_incorrect = pickle_reader('outputs/incorrect_net.pkl')
edge_data_passive = pickle_reader('outputs/passive_net.pkl')
edge_data_uncertain = pickle_reader('outputs/uncertain_net.pkl')
ttest_vals_ci = ttest_calc(edge_data_correct, edge_data_incorrect)
final_sig_vals_ci = find_significant_vals(ttest_vals_ci)
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
#print(final_sig_vals_uc)
write_dict('statistical_results/correctIncorrect.pkl', final_sig_vals_ci)
write_dict('statistical_results/correctPassive.pkl', final_sig_vals_cp)
write_dict('statistical_results/incorrectPassive.pkl', final_sig_vals_ip)
write_dict('statistical_results/correctUncertain.pkl', final_sig_vals_uc)
write_dict('statistical_results/incorrectuncertain.pkl', final_sig_vals_ui)
write_dict('statistical_results/passiveUncertain.pkl', final_sig_vals_up)



        

#.plot(*zip(*sorted(bc.items())))
#plt.show()
