# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we adjust parameters and run the model

=========================================================================== """

import generate_network as gn
import dynamics_network as dn
import analyze_network as an
import networkx as nx
import time

#NOTE: The print_stuff funtion got moved to the analyze_network file.
def printStuff(nodes):
    print("\n")
    for node in nodes:
        print(node)
#
## Build a network corresponding to regular grid with d dimensions of size L, 
## with liquidity threshold -4 and solvency threshold -6
network = gn.regular_network(L = 100,  d = 2, Tl = -4, Ts = -6)
#
avalanches = []
for i in range(30):
    print(i)
    avalanche_sizes = dn.run_simulation(network, 1000)
    for ava in avalanche_sizes:
        avalanches.append(ava)
    
avalanches.append()
## Plot the distribution of avalanches
an.histogram_avalanches(avalanches, num_bins = len(avalanches), y_scale='log', x_scale='linear')

# Plot the graph in a circle. NOTE: This only works on small graphs.
# an.plot_network(network)
#
#order = {}
#
#for node in network.nodes():
#    order[node.getLabel()] = node
#
#node0 = order[0]
#node1 = order[1]
#node2 = order[2]
#node3 = order[3]
#node4 = order[4]
#node5 = order[5]
#node6 = order[6]
#node7 = order[7]
#node8 = order[8]
#
#node6.setCapital(-3)
#node6.changeDebt(node3, -1)
#node6.changeDebt(node1, -2)
#
#node3.setCapital(3)
#node3.changeDebt(node6, 1)
#node3.changeDebt(node8, 1)
#node3.changeDebt(node5, 1)
#
#node5.setCapital(-3)
#node5.changeDebt(node3, -1)
#node5.changeDebt(node7, -2)
#
#node7.setCapital(3)
#node7.changeDebt(node5, 2)
#node7.changeDebt(node2, 1)
#
#node8.setCapital(-3)
#node8.changeDebt(node3, -1)
#node8.changeDebt(node1, -1)
#node8.changeDebt(node0, -1)
#
#node1.setCapital(5)
#node1.changeDebt(node6, 2)
#node1.changeDebt(node4, 2)
#node1.changeDebt(node8, 1)
#
#node2.setCapital(-1)
#node2.changeDebt(node0, 0)
#node2.changeDebt(node7, -1)
#
#node0.setCapital(1)
#node0.changeDebt(node4, 0)
#node0.changeDebt(node2, 0)
#node0.changeDebt(node8, 1)
#
#node4.setCapital(-2)
#node4.changeDebt(node0, 0)
#node4.changeDebt(node1, -2)
#
#
#
#printStuff(network.nodes())
##                 
#dn._check_and_propagate_avalanche(network, [])
##
#printStuff(network.nodes())


