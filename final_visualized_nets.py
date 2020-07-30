#import matplotlib.pylab as plt
#from networkx.algorithms.community import greedy_modularity_communities
#from networkx.algorithms.community import asyn_lpa_communities
import pickle
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import write_dot

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
        weight = whole_data[key]
        final_edges.update({source_str : {target_str : {'weight' : weight}}})
        
            
    return final_edges

def write_network_to_file(network, net_type):
    string_file_name = str('final_visual/' + net_type + ".dot")
    write_dot(network, string_file_name)


brain_groups = { 'visual cortex' : ["VISa", "VISam", "VISl", "VISp", "VISpm", "VISrl"], # visual cortex
                'thalamus' : ["CL", "LD", "LGd", "LH", "LP", "MD", "MG", "PO", "POL", "PT", "RT", "SPF", "TH", "VAL", "VPL", "VPM"], # thalamus
                'hippocampal' : ["CA", "CA1", "CA2", "CA3", "DG", "SUB", "POST"], # hippocampal
                'non-visual cortex' : ["ACA", "AUD", "COA", "DP", "ILA", "MOp", "MOs", "OLF", "ORB", "ORBm", "PIR", "PL", "SSp", "SSs", "RSP"," TT"], # non-visual cortex
                'midbrain' : ["APN", "IC", "MB", "MRN", "NB", "PAG", "RN", "SCs", "SCm", "SCig", "SCsg", "ZI"], # midbrain
                'basal ganglia' : ["ACB", "CP", "GPe", "LS", "LSc", "LSr", "MS", "OT", "SNr", "SI"], # basal ganglia 
                'cortical subplate' : ["BLA", "BMA", "EP", "EPd", "MEA"] # cortical subplate
                }

edge_data_ci = pickle_reader('statistical_results/correctIncorrect.pkl')
edges_ci = edge_gen(edge_data_ci)
edge_data_cp = pickle_reader('statistical_results/correctPassive.pkl')
edges_cp = edge_gen(edge_data_cp)
edge_data_cu = pickle_reader('statistical_results/correctUncertain.pkl')
edges_cu = edge_gen(edge_data_cu)
edge_data_ip = pickle_reader('statistical_results/incorrectPassive.pkl')
edges_ip = edge_gen(edge_data_ip)
edge_data_iu = pickle_reader('statistical_results/incorrectUncertain.pkl')
edges_iu = edge_gen(edge_data_iu)
edge_data_pu = pickle_reader('statistical_results/passiveUncertain.pkl')
edges_pu = edge_gen(edge_data_pu)
edge_data_ap = pickle_reader('statistical_results/activePassive.pkl')
edges_ap = edge_gen(edge_data_ap)
edge_data_ceu = pickle_reader('statistical_results/certainUncertain.pkl')
edges_ceu = edge_gen(edge_data_ceu)

final_regions = dict()

net_ci = nx.from_dict_of_dicts(edges_ci, create_using = nx.DiGraph())
for node in net_ci.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
#print(final_regions)                
nx.set_node_attributes(net_ci, final_regions, 'region')
#print(net_ci.nodes())

net_cp = nx.from_dict_of_dicts(edges_cp, create_using = nx.DiGraph())
final_regions = dict()
for node in net_cp.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
#print(final_regions)                
nx.set_node_attributes(net_cp, final_regions, 'region')
#print(net_ci.nodes())

net_cu = nx.from_dict_of_dicts(edges_cu, create_using = nx.DiGraph())
final_regions = dict()
for node in net_cu.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
#print(final_regions)                
nx.set_node_attributes(net_cu, final_regions, 'region')
#print(net_ci.nodes())

net_ip = nx.from_dict_of_dicts(edges_ip, create_using = nx.DiGraph())
final_regions = dict()
for node in net_ip.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
#print(final_regions)                
nx.set_node_attributes(net_ip, final_regions, 'region')
#print(net_ci.nodes())

net_iu = nx.from_dict_of_dicts(edges_iu, create_using = nx.DiGraph())
final_regions = dict()
for node in net_iu.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
#print(final_regions)                
nx.set_node_attributes(net_iu, final_regions, 'region')
#print(net_ci.nodes())

net_pu = nx.from_dict_of_dicts(edges_pu, create_using = nx.DiGraph())
final_regions = dict()
for node in net_pu.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
#print(final_regions)                
nx.set_node_attributes(net_pu, final_regions, 'region')
#print(net_ci.nodes())

net_ap = nx.from_dict_of_dicts(edges_ap, create_using = nx.DiGraph())
final_regions = dict()
for node in net_ap.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
#print(final_regions)                
nx.set_node_attributes(net_ap, final_regions, 'region')
#print(net_ci.nodes())
final_regions = dict()

net_ceu = nx.from_dict_of_dicts(edges_ceu, create_using = nx.DiGraph())
for node in net_cu.nodes():
    area = str(node)
    for key in brain_groups.keys():
        for area_str in brain_groups[key]:
            if area == area_str:
                final_regions[node] = key
#print(final_regions)                
nx.set_node_attributes(net_ceu, final_regions, 'region')

write_network_to_file(net_ci, 'ci')
write_network_to_file(net_cp, 'cp')
write_network_to_file(net_cu, 'cu')
write_network_to_file(net_ip, 'ip')
write_network_to_file(net_iu, 'iu')
write_network_to_file(net_pu, 'pu')
write_network_to_file(net_ap, 'ap')
write_network_to_file(net_ceu, 'ceu')



        

#.plot(*zip(*sorted(bc.items())))
#plt.show()
