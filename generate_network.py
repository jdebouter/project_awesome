# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we define the functions for generating the network. 

=========================================================================== """

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

''' Generate and return a network that corresponds to a regular lattice
    with dimension d and dimensions with size L.
    Tl is the liquidity threshold and Ts the solvency threshold. '''
def regular_network(L, d, Tl, Ts):
    # Build the graph
    G = nx.grid_graph([L for i in range(d)], periodic=False)
    # Add the extra attributes we need
    _addAttributes(G, Tl, Ts)
    return G

''' Generate and return a random network of size N with link probability p.
    Tl is the liquidity threshold and Ts the solvency threshold. '''
def random_network(N, p, Tl, Ts):
    G = nx.erdos_renyi_graph(N, p)
    _addAttributes(G, Tl, Ts)
    return G

''' Generate and return a scale-free network of size N and with m the number 
    of edges that are added to new nodes each iteration during growth of the 
    network.
    Tl is the liquidity threshold and Ts the solvency threshold. '''
def barabasi_albert_network(N, m, Tl, Ts):
    G = nx.barabasi_albert_graph(N, m)
    _addAttributes(G, Tl, Ts)
    return G

''' Generate and return a scale-free network of size N using the mean field
    algorithm. 
    The algorithm is described in section 3 of the paper "Self-similarity of 
    Banking Networks" which is in the google drive folder.
    Tl is the liquidity threshold and Ts the solvency threshold. 
    c impacts the number of nodes (See paper for more info).
    m impacts the number of hubs (See paper for more info).
    NOTE: I would suggest not changing c and m, because the algorithm is quite 
    sensitive to there values. 
    '''
def mean_field_network(N, Tl, Ts, c = 1, m = 0.52):
    G = _mean_field_graph(N, Tl, Ts, c, m)
    _addAttributes(G, Tl, Ts)
    return G


''' Add all of the attributes like banking capital theta and thresholds to the
    graph, nodes and dges '''
def _addAttributes(G, Tl, Ts):
    # Add the liquidity threshold and solvency threshold
    G.graph['Tl'] = Tl
    G.graph['Ts'] = Ts
    # Add banking capital attribute and bankruptcy attributes to all nodes (initialize at 0 and False)
    nx.set_node_attributes(G, 'capital', 0)
    nx.set_node_attributes(G, 'liquidity', 0)
    nx.set_node_attributes(G, 'bankrupt', False)
    # Add a debt attribute to every edge (and attributes describing to whom the debt is owed)
    nx.set_edge_attributes(G, 'debt', 0)
    nx.set_edge_attributes(G, 'lender', None)
    nx.set_edge_attributes(G, 'borrower', None)


""" ===========================================================================

The remaining functions are used to generate the mean field network.
The algorithm is described in section 3 of the paper "Self-similarity of 
Banking Networks" which is in the Google Drive folder. I have tried to use
the same notation as in the paper. Roughly speaking the algorithm generates
the network by assigning a random credit rating to each node and then edges 
are more likely between banks with good credit ratings.

=========================================================================== """

'''
    Compute w(t) as described in the paper such that:
        w_{i,j}(t) = m_i(t) * m_j(t)'''
def _compute_w(bank_credit_ratings):
    N = len(bank_credit_ratings)
    to_return = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            # Equation 3 in the paper.
            to_return[i, j] = bank_credit_ratings[i] * bank_credit_ratings[j]
    return to_return

'''
    Compute the sorted and normalized m values. '''
def _compute_credit_ratings(N):
    credit_ratings = np.random.rand(N)
    credit_ratings = credit_ratings / np.sum(credit_ratings)
    credit_ratings = np.sort(credit_ratings)[::-1]
    return credit_ratings
'''
    Iteratively solve for for w matrix. '''
def _compute_lending_freq(credit_ratings, m):
    N = len(credit_ratings)
    w = _compute_w(credit_ratings)
    for t in range(1000):
        for i in range(N):
            # Equation 4 in the paper.
            credit_ratings[i] = np.sum(w[i, i+1:]) + m / N
        # Equation 5 in the paper.
        credit_ratings = credit_ratings / np.sum(credit_ratings) 
        w = _compute_w(credit_ratings)
    return w
'''
    A wrapper function combining all the necessary pieces required
    to generate the mean field graph.'''
def _mean_field_graph(N, Tl, Ts, c, m):
    # Init Graph 
    G = nx.Graph()
    G.add_nodes_from([0, N-1])
    # Compute the credit ratings (m) and lending_freq (w).
    credit_ratings = _compute_credit_ratings(N)
    lending_freq = _compute_lending_freq(credit_ratings, m)
    # Use the credit ratings and lending_freq to add edges.
    w_t = c * min(credit_ratings) * max(credit_ratings)
    for i in range(N):
        for j in range(i, N):
            if lending_freq[i, j] >= w_t:
                G.add_edge(i, j)
    return G







