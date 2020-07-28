#import matplotlib.pylab as plt
#from networkx.algorithms.community import greedy_modularity_communities
#from networkx.algorithms.community import asyn_lpa_communities
import pickle
import networkx as nx
import pydot

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
net_ci = nx.from_dict_of_dicts(edges_ci, create_using = nx.DiGraph())
net_cp = nx.from_dict_of_dicts(edges_cp, create_using = nx.DiGraph())
net_cu = nx.from_dict_of_dicts(edges_cu, create_using = nx.DiGraph())
net_ip = nx.from_dict_of_dicts(edges_ip, create_using = nx.DiGraph())
net_iu = nx.from_dict_of_dicts(edges_iu, create_using = nx.DiGraph())
net_pu = nx.from_dict_of_dicts(edges_pu, create_using = nx.DiGraph())

write_network_to_file(net_ci, 'ci')
write_network_to_file(net_cp, 'cp')
write_network_to_file(net_cu, 'cu')
write_network_to_file(net_ip, 'ip')
write_network_to_file(net_iu, 'iu')
write_network_to_file(net_pu, 'pu')



        

#.plot(*zip(*sorted(bc.items())))
#plt.show()
