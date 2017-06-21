# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we adjust parameters and run the model

=========================================================================== """

import generate_network as gn
import dynamics_network as dn
import analyze_network as an
import networkx as nx

#NOTE: The print_stuff funtion got moved to the analyze_network file.

# Build a network corresponding to regular grid with d dimensions of size L, 
# with liquidity threshold -4 and solvency threshold -6
network = gn.regular_network(L = 100, d = 2, Tl = -2, Ts = -4)

# Run the simulation for 100 iteration
avalanche_sizes = dn.run_simulation(network, 100)

# Plot the distribution of avalanches
an.histogram_avalanches(avalanche_sizes, num_bins = 10)

# Plot the graph in a circle. NOTE: This only works on small graphs.
# an.plot_network(network)



