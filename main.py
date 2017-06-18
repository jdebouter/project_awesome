# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we adjust parameters and run the model
(although I think it makes sense to define the details of running the model in
dynamics_network.py)

=========================================================================== """

import generate_network as gn
import dynamics_network as dn
import networkx as nx
import matplotlib.pyplot as plt

# Build a network corresponding to a 5x5 regular grid with liquidity
# threshold Tl and solvency threshold -6
network = gn.regular_network(5, 2, Tl = -4, Ts = -6)

# Debug/print
for item in list(network.edges(data=True)):
    print(item)

# Draw the graph. NOTE: networkx has some basic drawing functionality but it
# takes too long for me to draw 100x100
#nx.draw(G)
#plt.show()