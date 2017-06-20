# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we adjust parameters and run the model

=========================================================================== """

import generate_network as gn
import dynamics_network as dn
import networkx as nx
import matplotlib.pyplot as plt

# Build a network corresponding to regular grid with d dimensions of size L, 
# with liquidity threshold -4 and solvency threshold -6
network = gn.regular_network(L = 3, d = 2, Tl = -4, Ts = -6)

# DEBUG
dn._perturb(network)
for node in network.nodes_iter(data=True):
    print(node)
print()
for edge in network.edges_iter(data=True):
    print(edge)
    
dn._invest_surplus_liquidity(network)
print("\n\n\n")
for node in network.nodes(data=True):
    print(node)
print()
for edge in network.edges_iter(data=True):
    print(edge)

# Run the simulation for 1 iteration
#dn.run_simulation(network, 1)

# Draw the graph. NOTE: networkx has some basic drawing functionality but it
# takes too long for me to draw 100x100
#nx.draw(G)
#plt.show()