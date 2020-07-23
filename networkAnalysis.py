import igraph
import numpy as np
import networkx as nx

# ------------------------------------------------------------------#


def multilevel(adj_matrix, directed=False, return_levels=False):
    """
    find communities of given weighted adjacency network

    :param adjMatrix: [2d array] adjacency matrix  
    :param directed: [bool(default=False)] choose directed or undirected network
    :param return_levels: if True, the communities at each level are returned in a list. If False, only the community structure with the best modularity is returned.
    :return: a list of VertexClustering objects, one corresponding to each level (if return_levels is True), or a VertexClustering corresponding to the best modularity.
    """

    conn_indices = np.where(adj_matrix)
    weights = adj_matrix[conn_indices]
    edges = zip(*conn_indices)
    G = igraph.Graph(edges=edges, directed=directed)
    G.es['weight'] = weights
    comm = G.community_multilevel(
        weights=weights, return_levels=return_levels)

    return comm

# ---------------------------------------------------------------#


def walktrap(adj, steps=5):
    """
    Community detection algorithm of Latapy & Pons, based on random walks. The basic idea of the algorithm is that short random walks tend to stay in the same community. The result of the clustering will be represented as a dendrogram.

    :param adj: name of an edge attribute or a list containing edge weights
    :param steps: length of random walks to perform
    :return: a L{VertexDendrogram} object, initially cut at the maximum  modularity.

    :Reference: 

    -  Pascal Pons, Matthieu Latapy: Computing communities in large networks using random walks, U{http://arxiv.org/abs/physics/0512106}.

    >>> adj = np.random.rand(20, 20)
    >>> print(walktrap(adj))
    >>> # Clustering with 20 elements and 2 clusters
    >>> # [0] 0, 5, 8, 10, 19
    >>> # [1] 1, 2, 3, 4, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18

    """

    conn_indices = np.where(adj)
    weights = adj[conn_indices]
    edges = list(zip(*conn_indices))
    G = igraph.Graph(edges=edges, directed=False)
    comm = G.community_walktrap(weights, steps=steps)
    communities = comm.as_clustering()

    # print comm
    # print("%s number of clusters = %d " % (
    #     label, len(communities)))
    # print "optimal count : ", comm.optimal_count

    return communities
# ------------------------------------------------------------------#


def calculate_NMI(self, comm1, comm2, method="nmi"):
    """
    Compares two community structures

    :param comm1: the first community structure as a membership list or as a Clustering object.
    :param comm2: the second community structure as a membership list or as a Clustering object.
    :param method: [string] defaults to ["nmi"] the measure to use. "vi" or "meila" means the variation of information metric of Meila (2003), "nmi" or "danon" means the normalized mutual information as defined by Danon et al (2005), "split-join" means the split-join distance of van Dongen (2000), "rand" means the Rand index of Rand (1971), "adjusted_rand" means the adjusted Rand index of Hubert and Arabie (1985).
    :return: [float] the calculated measure.

    Reference: 

    -  Meila M: Comparing clusterings by the variation of information. In: Scholkopf B, Warmuth MK (eds). Learning Theory and Kernel Machines: 16th Annual Conference on Computational Learning Theory and 7th Kernel Workship, COLT/Kernel 2003, Washington, DC, USA. Lecture Notes in Computer Science, vol. 2777, Springer, 2003. ISBN: 978-3-540-40720-1.

    -  Danon L, Diaz-Guilera A, Duch J, Arenas A: Comparing community structure identification. J Stat Mech P09008, 2005.

    -  van Dongen D: Performance criteria for graph clustering and Markov cluster experiments. Technical Report INS-R0012, National Research Institute for Mathematics and Computer Science in the Netherlands, Amsterdam, May 2000.

    -  Rand WM: Objective criteria for the evaluation of clustering methods. J Am Stat Assoc 66(336):846-850, 1971.

    -  Hubert L and Arabie P: Comparing partitions. Journal of Classification 2:193-218, 1985.
    """

    nmi = igraph.compare_communities(
        comm1, comm2, method='nmi', remove_none=False)
    return nmi
# ------------------------------------------------------------------#
