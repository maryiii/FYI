import pydot
from networkx.drawing.nx_pydot import read_dot
import networkx as nx
import os
import pickle

def load_data(path):
    network = read_dot(path)
    return network

def list_of_section_areas(network):
    dict_areas = nx.get_node_attributes(network, 'area')
    unique_area_value = [] 
    for area in dict_areas.values():
        if area in unique_area_value:
            continue 
        else:
            unique_area_value.append(area)
    return unique_area_value

def brain_region(network, area):
    nodes_at_area = [x for x,y in network.nodes(data=True) if y['area'] == area]
    area_subgraph = network.subgraph(nodes_at_area)
    return area_subgraph

def within_weights(area_network):
    
    normalization_val = area_network.size() 
    if(normalization_val == 0):
        return 0;
    sum_of_internal_weights = 0
    
    for val in nx.get_edge_attributes(area_network, 'weight').values():
        val = val.replace('"','')
        #print (val)
        sum_of_internal_weights += float(val)
    
    #print(nx.get_edge_attributes(area_network, 'weight').values())
    return sum_of_internal_weights / normalization_val

def between_weights(whole_network, area_network1, source_area, dict_of_final_edges):
    for node in area_network1.nodes:
        for neighbor in whole_network.neighbors(node):
            if not(area_network1.has_node(neighbor)):
                dest_area = whole_network.nodes()[neighbor]['area']
                key_val = source_area + ',' + dest_area
                we = float(whole_network[node][neighbor][0]['weight'].replace('"', ''))
                if key_val in dict_of_final_edges.keys():
                    #print(whole_network[node][neighbor][0]['weight'])
                    dict_of_final_edges[key_val][0] += we
                    dict_of_final_edges[key_val][1] += 1
                    #print(dict_of_final_edges[key_val])
                else:
                   #print(whole_network[node][neighbor][0]['weight'])
                    dict_of_final_edges[key_val] = [we, 1.0]
                    #print(dict_of_final_edges[key_val])
    return dict_of_final_edges 
                    
def avg_edges(dict_edges):
    final_edges = dict()
    #print(dict_edges)
    i = 0
    for key_area in dict_edges.keys():
        #print(key_area, ', ', dict_edges[key_area])
        final_edges[key_area] = dict_edges[key_area][0] / dict_edges[key_area][1]
        i+=1
        
    return final_edges

def run_sections(pattern):
    directory = './data' 
    last_final_edges_dict = dict() 
    for filename in os.listdir(directory):
        if filename.endswith(pattern):
            #f = open(filename)
            print(filename)               
            network = load_data('data/' + filename)
            list_areas = list_of_section_areas(network)
            dict_of_final_edges = dict()
            
            #print(list_areas)
            #print(within_weights(network))
            
            for area in list_areas:
                #print(area)
                brain_area_network = brain_region(network, area)
                dict_of_final_edges[area + ',' + area] = [within_weights(brain_area_network), 1]
                #print(dict_of_final_edges[area + ',' + area])
                dict_of_final_edges.update(between_weights(network, brain_area_network, area, dict_of_final_edges))
                
                #print(dict_of_final_edges)
            dict_of_final_edges = avg_edges(dict_of_final_edges)
                
                #print(dict_of_final_edges)
            for key in dict_of_final_edges.keys():
                if key in last_final_edges_dict:
                    last_final_edges_dict[key].append(dict_of_final_edges[key])
                else:
                    #print(dict_of_final_edges[key])
                    last_final_edges_dict[key] = [dict_of_final_edges[key]]
                    #print(last_final_edges_dict)
                            
    return last_final_edges_dict

def write_dict(name, dict_of_final_edges):
    f = open(name, 'wb')
    pickle.dump(dict_of_final_edges, f)
    f.close()

final_correct_edges = run_sections("cnet.dot")
write_dict('outputs/correct_net.pkl', final_correct_edges)