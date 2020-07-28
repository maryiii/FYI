import numpy as np
import networkx as nx
#import matplotlib.pylab as plt
#from networkx.algorithms.community import greedy_modularity_communities
#from networkx.algorithms.community import asyn_lpa_communities
import pickle
#import community as community_louvain
#from networkx.algorithms.community import asyn_lpa_communities
import pydot
from networkx.drawing.nx_pydot import write_dot
import re
import os 

def get_numbers_from_filename(filename):
    return re.search(r'\d+', filename).group(0)

#read the input data from .pkl file into a dictionary
def pickle_reader(file):
    with open(file, 'rb') as handle:
        whole_data = pickle.load(handle)
    
    return whole_data

#return adjancy matrix for one of the three networks
def net_adj_matrix(whole_data, net_type):
    net = whole_data[net_type]
    correct_net_adj_matrix = net[:,:,0]
    #print(net, net.shape)
    #print(correct_net_adj_matrix.shape)
    return correct_net_adj_matrix

#return dictionary of each nodes area
def brain_area_attr(whole_data, net_type):
    dict_of_neuron_area = dict()
    net = whole_data[net_type]
    for i in range(len(net)):
        dict_of_neuron_area[i] = { 'area' : net[i]}
        
    return dict_of_neuron_area

def pairwise_delay(whole_data, net_type):
    net = whole_data[net_type]
    network_of_pairwise_delay = net[:,:,1]
    dict_of_delays = dict()
    for i in range(network_of_pairwise_delay.shape[0]):
        for j in range(network_of_pairwise_delay.shape[1]):
            dict_of_delays[(i, j)] = {'delay' : network_of_pairwise_delay[i,j]}  
    return dict_of_delays

def edge_optimization(whole_data, net_type):
    net = whole_data[net_type]
    net_adj = net_adj_matrix(whole_data, net_type)
    p_val_edges = net[:, :, 2]
    for i in range(p_val_edges.shape[0]):
        for j in range(p_val_edges.shape[1]):
            if p_val_edges[i, j] > 0.05:
                net[i, j] = 0
                    
    return net_adj
   
def degree_calculator(net):
	dict_of_nodes = dict()

	for node in net.nodes():
		in_degree = net.in_degree(node)
		out_degree = net.out_degree(node)
	
		dict_of_nodes[node] = [in_degree, out_degree, out_degree - in_degree]

		#print(dict_of_nodes[node])
	
	return dict_of_nodes

def add_bt_centrality_neuron(network):
    
    bc = nx.betweenness_centrality(network, weight = 'weight')
    for key in bc.keys():
        bc[key] = {'Betweenness_centrality' : bc[key]}
    
    nx.set_node_attributes(network, bc)
    #community_finder(network)
    
    print(network.nodes[0])
    
    
def write_network_to_file(network, net_type):
    string_file_name = str(net_type + ".dot")
    write_dot(network, string_file_name)
    
def graph_generator(whole_data, net_type, net_areas):
    network = edge_optimization(whole_data, net_type)
    final_network = nx.from_numpy_array(network, create_using=nx.DiGraph())
    node_areas = brain_area_attr(whole_data, net_areas)
    print(node_areas)
    nx.set_node_attributes(final_network, values = node_areas)
    edge_delays = pairwise_delay(whole_data, net_type)
    #print(edge_delays)
    nx.set_edge_attributes(final_network, edge_delays)
    add_bt_centrality_neuron(final_network)
    return final_network
    
    #print(final_network.number_of_nodes())
    #print(final_network[164][161])
    
'''    
def community_finder(network):
    partion = community_louvain.best_partition(network)
'''        





#print(sorted(greedy_modularity_communities(net1, weight = 'weight')[0]))
#print(len(greedy_modularity_communities(net1, weight = 'weight')))
'''
for d in asyn_lpa_communities(net1, 'weight'):
	print(d)
    com = next(d)
    print(len(com))
    for p in com:
        nt(com)
'''

#print(pickle_reader('NetResults_3.pkl'))
for filename in os.listdir('C:/Users/ansar/Desktop/information_flow/FYI/Networks'):
    file_number = get_numbers_from_filename(filename)
    network_data = pickle_reader('Networks/NetResults_' + file_number + '.pkl')
    '''
    graph_correct = graph_generator(network_data, 'Correct Network', 'Correct Brain Areas')
    #print(nx.get_edge_attributes(graph_correct, 'delay
    graph_incorrect = graph_generator(network_data, 'Incorrect Network', 'Incorrect Brain Areas')
    graph_passive = graph_generator(network_data, 'Passive Network', 'Passive Brain Areas')
    '''
    graph_uncertain = graph_generator(network_data, 'Uncertain Network', 'Uncertain Brain Areas')
    '''
    write_network_to_file(graph_correct, "data/correct" + file_number + "_cnet")
    write_network_to_file(graph_incorrect, "data/incorrect" + file_number + "_inet")
    write_network_to_file(graph_passive, "data/passive" + file_number + "_pnet")
    '''
    write_network_to_file(graph_uncertain, "data/uncertain" + file_number + "_unet")

#.plot(*zip(*sorted(bc.items())))
#plt.show()