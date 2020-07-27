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


edge_data = pickle_reader('outputs/correct_net.pkl')
edge_data1 = pickle_reader('outputs/incorrect_net.pkl')

final_stats = dict()
for key in edge_data.keys():
    if key in edge_data1.keys():
        list_1 = edge_data[key]
        print(list_1)
        list_2 = edge_data1[key]
        print(list_2)
        final_stats[key] = stats.ttest_ind(a=list_1,b=list_2,equal_var=True)
print(final_stats)

#.plot(*zip(*sorted(bc.items())))
#plt.show()