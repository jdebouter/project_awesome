# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we define the functions for generating the network. 

=========================================================================== """

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import WithoutNetworks as kk

''' Generate and return a network that corresponds to a regular lattice
    with dimension d and dimensions with size L.
    Tl is the liquidity threshold and Ts the solvency threshold. '''
def regular_network(L, d, Tl, Ts):
    # Build the graph, ie get the topology
    G = nx.grid_graph([L for i in range(d)], periodic=False)
    # Topology is done, but now replace the nodes (just tuples) with Bank objects
    return _replaceNodesWithBankObjects(G, Tl, Ts)

''' Generate and return a random network of size N with link probability p.
    Tl is the liquidity threshold and Ts the solvency threshold. '''
def random_network(N, p, Tl, Ts):
    G = nx.erdos_renyi_graph(N, p)
    return _replaceNodesWithBankObjects(G, Tl, Ts)

''' Generate and return a scale-free network of size N and with m the number 
    of edges that are added to new nodes each iteration during growth of the 
    network.
    Tl is the liquidity threshold and Ts the solvency threshold. '''
def barabasi_albert_network(N, m, Tl, Ts):
    G = nx.barabasi_albert_graph(N, m)
    return _replaceNodesWithBankObjects(G, Tl, Ts)

''' Generate and return a scale-free network of size N using the mean field
    algorithm. 
    The algorithm is described in section 3 of the paper "Self-similarity of 
    Banking Networks" which is in the google drive folder.
    Tl is the liquidity threshold and Ts the solvency threshold. 
    c impacts the number of nodes (See paper for more info).
    m impacts the number of hubs (See paper for more info).
    NOTE: I would suggest not changing c and m, because the algorithm is quite 
    sensitive to their values. 
    '''
def mean_field_network(N, Tl, Ts, c = 1, m = 0.52):
    G = _mean_field_graph(N, Tl, Ts, c, m)
    return _replaceNodesWithBankObjects(G, Tl, Ts)


''' Add all of the attributes like banking capital theta and thresholds to the
    graph, nodes and dges '''
    
def _replaceNodesWithBankObjects(G, Tl, Ts):
    banks = initializeBanks(G.number_of_nodes())
    # Add the liquidity threshold and solvency threshold
    G.graph['Tl'] = Tl
    G.graph['Ts'] = Ts
    return linkBanks(G, banks)

# Define the banking grid with a unbalanced grid
def initializeBanks(tot_banks):
    banks = []
#    capital = range(-2, 3)
    for i in range(tot_banks):
#        bank = Bank(i, random.choice(capital))
        bank = kk.Bank(i, 0)
        banks.append(bank)
#    maximum_neighbours = 4
#    assignNeighbours(banks, maximum_neighbours)
    return banks


def linkBanks(G, banks):
    """
    Objects of the Bank class are assigned as Nodes
    Also, a adjacency matrix for this network is printed
    """
    
    # Relabelling the nodes to that of the objects of the class Bank
    mapping = dict(zip(G.nodes(), banks))
    grid = nx.relabel_nodes(G, mapping)
    # Assigning a position to banks according to the ordering in the network
    i = 0
    for nodes in grid.nodes():
        nodes.setPosition(i)
        i += 1
    # Creating the adjacency matrix
#    print(createAdjacencyMatrix(grid))
    # Drawing the graph
    bank_positions = [nodes.getLabel() for nodes in grid.nodes()]
    bank_labels = dict(zip(grid.nodes(), bank_positions))
#    nx.draw(grid, labels = bank_labels, with_labels = True)
#    plt.show()
    _assignNeighbours(grid)
    
    return grid

# Neighbours are assignmed  
def _assignNeighbours(network):
    for node in network.nodes():
        node.putNeighbours(network.neighbors(node),[0]*len(network.neighbors(node)))

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
    FG = _addBanks(G, Tl, Ts)
    return FG







