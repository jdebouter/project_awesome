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

# Build a network corresponding to regular grid with d dimensions of size L, 
# with liquidity threshold -4 and solvency threshold -6
network = gn.regular_network(L = 2, d = 2, Tl = -4, Ts = -6)

# Debug/print
#for item in list(network.nodes(data=True)):
#    print(item)

# Run the simulation for 1 iteration
dn.run_simulation(network, 1)

# Draw the graph. NOTE: networkx has some basic drawing functionality but it
# takes too long for me to draw 100x100
#nx.draw(G)
#plt.show()