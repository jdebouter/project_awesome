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
network.node[(0,0)]['liquidity'] = 4
network.edge[(0,0)][(0,1)]['debt'] = 5
network.edge[(0,0)][(0,1)]['borrower'] = (0,0)
network.edge[(0,0)][(0,1)]['loaner'] = (0,1)
network.edge[(0,0)][(1,0)]['debt'] = 3
network.edge[(0,0)][(1,0)]['borrower'] = (0,0)
network.edge[(0,0)][(1,0)]['loaner'] = (1,0)


for node in network.nodes(data=True):
    print(node)
print(network.edge[(0,0)][(0,1)])
print(network.edge[(0,0)][(1,0)])

dn._repay_debts(network)

print("\n")
for node in network.nodes(data=True):
    print(node)
print(network.edge[(0,0)][(0,1)])
print(network.edge[(0,0)][(1,0)])

# Run the simulation for 1 iteration
#dn.run_simulation(network, 1)

# Draw the graph. NOTE: networkx has some basic drawing functionality but it
# takes too long for me to draw 100x100
#nx.draw(G)
#plt.show()