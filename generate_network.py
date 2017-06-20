# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we define the functions for generating the network. 

=========================================================================== """

import networkx as nx

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
    nx.set_edge_attributes(G, 'loaner', None)
    nx.set_edge_attributes(G, 'borrower', None)