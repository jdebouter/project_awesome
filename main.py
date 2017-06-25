# -*- coding: utf-8 -*-
""" ===========================================================================
This script is where we adjust parameters and run the model
=========================================================================== """
import generate_network as gn
import dynamics_network as dn
import analyze_network as an
import networkx as nx

''' Parameters that change the implementation a little:
    quick_repaying = True/False. True means that banks will repay a debt if 
        that happen to get a surplus that round, even if they have negative 
        liquidity. False means that they'll only repay if they have positive 
        capital/liquidity 
    (UNFINISHED)
    transfer_pattern - node_by_node/evenly_distributed. 'node_by_node' means
        that some random node is chosen and all debt/loan is repayed / collected
        until balance is regained. 'evenly_distributed' means that they'll try
        to repay/collect from all borrowers/lenders evenly
        back any money that was lost. 
    too_big_to_fail - policy, more description later...'''
parameters = {"quick_repaying" : True,
              "diversify_trade" : True,
              "too_big_to_fail" : False}  # (This one is useless in a regular grid)

## Build a network 
network = gn.regular_network(L = 20, d = 2, Tl = -4, Ts = -6)
 
avalanche_sizes = dn.run_simulation(network, 100, parameters, DEBUG_BOOL = True)

#avalanche_sizes = []
#for i in range(1):
#    network = gn.regular_network(L = 10, d = 4, Tl = -7, Ts = -10)
#    sizes = dn.run_simulation(network, 1000, parameters)
#    # Remove first 10%
#    sizes = sizes[int(len(sizes) / 10.0) : ]
#    avalanche_sizes = avalanche_sizes + sizes

## Plot the distribution of avalanches
an.histogram_avalanches(avalanche_sizes, num_bins = 100, y_scale='log', x_scale='linear')
an.histogram_avalanches(avalanche_sizes, num_bins = 100, y_scale='log', x_scale='log')