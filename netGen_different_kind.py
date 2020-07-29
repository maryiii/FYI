#import matplotlib.pylab as plt
#from networkx.algorithms.community import greedy_modularity_communities
#from networkx.algorithms.community import asyn_lpa_communities
import pickle
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import write_dot
import numpy as np

#import community as community_louvain
#from networkx.algorithms.community import asyn_lpa_communities

#read the input data from .pkl file into a dictionary
def pickle_reader(file):
    with open(file, 'rb') as handle:
        whole_data = pickle.load(handle)
    
    return whole_data


def edge_gen(whole_data):
    final_edges = dict()
    for key in whole_data.keys():
        source_str = str(key).split(',')[0]
        #print(source_str)
        target_str = str(key).split(',')[1]
        weight = np.mean(whole_data[key])
        final_edges.update({source_str : {target_str : {'weight' : weight}}})
        
            
    return final_edges

def write_network_to_file(network, net_type):
    string_file_name = str('final_visual/different_kinds/' + net_type + ".dot")
    write_dot(network, string_file_name)



brain_groups = { 'visual cortex' : ["VISa", "VISam", "VISl", "VISp", "VISpm", "VISrl"], # visual cortex
                'thalamus' : ["CL", "LD", "LGd", "LH", "LP", "MD", "MG", "PO", "POL", "PT", "RT", "SPF", "TH", "VAL", "VPL", "VPM"], # thalamus
                'hippocampal' : ["CA", "CA1", "CA2", "CA3", "DG", "SUB", "POST"], # hippocampal
                'non-visual cortex' : ["ACA", "AUD", "COA", "DP", "ILA", "MOp", "MOs", "OLF", "ORB", "ORBm", "PIR", "PL", "SSp", "SSs", "RSP"," TT"], # non-visual cortex
                'midbrain' : ["APN", "IC", "MB", "MRN", "NB", "PAG", "RN", "SCs", "SCm", "SCig", "SCsg", "ZI"], # midbrain
                'basal ganglia' : ["ACB", "CP", "GPe", "LS", "LSc", "LSr", "MS", "OT", "SNr", "SI"], # basal ganglia 
                'cortical subplate' : ["BLA", "BMA", "EP", "EPd", "MEA"] # cortical subplate
                }


edge_data_correct = pickle_reader('outputs/correct_net.pkl')
edges_correct = edge_gen(edge_data_correct)
edge_data_incorrect = pickle_reader('outputs/incorrect_net.pkl')
edges_incorrect = edge_gen(edge_data_incorrect)
edge_data_passive = pickle_reader('outputs/passive_net.pkl')
edges_passive = edge_gen(edge_data_passive)
edge_data_uncertain = pickle_reader('outputs/uncertain_net.pkl')
edges_uncertain = edge_gen(edge_data_uncertain)


net_correct = nx.from_dict_of_dicts(edges_correct, create_using = nx.DiGraph())
final_regions = dict()
for node in net_correct.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
nx.set_node_attributes(net_correct, final_regions, 'region')
net_incorrect = nx.from_dict_of_dicts(edges_incorrect, create_using = nx.DiGraph())
final_regions = dict()
for node in net_incorrect.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
nx.set_node_attributes(net_incorrect, final_regions, 'region')
net_passive = nx.from_dict_of_dicts(edges_passive, create_using = nx.DiGraph())
final_regions = dict()
for node in net_passive.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
nx.set_node_attributes(net_passive, final_regions, 'region')
net_uncertain = nx.from_dict_of_dicts(edges_uncertain, create_using = nx.DiGraph())
final_regions = dict()
for node in net_uncertain.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
nx.set_node_attributes(net_uncertain, final_regions, 'region')


write_network_to_file(net_correct, 'correct')
write_network_to_file(net_incorrect, 'incorrect')
write_network_to_file(net_passive, 'passive')
write_network_to_file(net_uncertain, 'uncertain')




        

#.plot(*zip(*sorted(bc.items())))
#plt.show()
