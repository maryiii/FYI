import pydot
from networkx.drawing.nx_pydot import read_dot
import networkx as nx
import os
import pickle

def load_data(path):
    network = read_dot(path)
    return network

def in_brain_group(network):
    brain_groups = { 'visual cortex' : ["VISa", "VISam", "VISl", "VISp", "VISpm", "VISrl"], # visual cortex
                'thalamus' : ["CL", "LD", "LGd", "LH", "LP", "MD", "MG", "PO", "POL", "PT", "RT", "SPF", "TH", "VAL", "VPL", "VPM"], # thalamus
                'hippocampal' : ["CA", "CA1", "CA2", "CA3", "DG", "SUB", "POST"], # hippocampal
                'non-visual cortex' : ["ACA", "AUD", "COA", "DP", "ILA", "MOp", "MOs", "OLF", "ORB", "ORBm", "PIR", "PL", "SSp", "SSs", "RSP"," TT"], # non-visual cortex
                'midbrain' : ["APN", "IC", "MB", "MRN", "NB", "PAG", "RN", "SCs", "SCm", "SCig", "SCsg", "ZI"], # midbrain
                'basal ganglia' : ["ACB", "CP", "GPe", "LS", "LSc", "LSr", "MS", "OT", "SNr", "SI"], # basal ganglia 
                'cortical subplate' : ["BLA", "BMA", "EP", "EPd", "MEA"] # cortical subplate
                }
    final_regions = dict()
    matched = False
    areas_of_network = nx.get_node_attributes(network, 'area')
    for key in areas_of_network:
        area = areas_of_network[key]
        for key_region in brain_groups.keys():
            for area_str in brain_groups[key_region]:
                if area == area_str:
                    final_regions[key] = key_region
                    matched = True
        if matched == False:
            final_regions[key] = 'other'
        matched = False 
                    
    nx.set_node_attributes(network, final_regions, 'region')
    return network

def remove_root(network):
    dict_of_areas = nx.get_node_attributes(network, 'area')
    for key in dict_of_areas:
        if dict_of_areas[key] == 'root':
            network.remove_node(key)
    return network

def list_of_regions(network):
    dict_regions = nx.get_node_attributes(network, 'region')
    unique_region_value = [] 
    for region in dict_regions.values():
        if region in unique_region_value:
            continue 
        else:
            unique_region_value.append(region)
    return unique_region_value
    

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

def brain_final_region(network, region):
    nodes_at_region = [x for x,y in network.nodes(data=True) if y['region'] == region]
    region_subgraph = network.subgraph(nodes_at_region)
    return region_subgraph

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
                dest_area = whole_network.nodes()[neighbor]['region']
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
            network_w_root = remove_root(network)
            updated_network = in_brain_group(network_w_root)
            list_regions = list_of_regions(updated_network)
            #list_areas = list_of_section_areas(network)
            dict_of_final_edges = dict()
            
            #print(list_areas)
            #print(within_weights(network))
            
            for region in list_regions:
                #print(area)
                brain_region_network = brain_final_region(updated_network, region)
                dict_of_final_edges[region + ',' + region] = [within_weights(brain_region_network), 1]
                #print(dict_of_final_edges[area + ',' + area])
                dict_of_final_edges.update(between_weights(updated_network, brain_region_network, region, dict_of_final_edges))
                
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
write_dict('outputs/regions/correct_net.pkl', final_correct_edges)
final_incorrect_edges = run_sections("inet.dot")
write_dict('outputs/regions/incorrect_net.pkl', final_incorrect_edges)
final_passive_edges = run_sections("pnet.dot")
write_dict('outputs/regions/passive_net.pkl', final_passive_edges)
final_uncertain_edges = run_sections("unet.dot")
write_dict('outputs/regions/uncertain_net.pkl', final_uncertain_edges)