# -*- coding: utf-8 -*-
""" ===========================================================================
This script is where we adjust parameters and run the model
=========================================================================== """
import generate_network as gn
import dynamics_network as dn
import analyze_network as an
import networkx as nx
import pickle

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
    panic_collection - True/False. 'True' means that infected bank collects
        collects money from all its borrower. 'False' means that bank only collects 
        back the lost capital
    too_big_to_fail - policy, more description later...'''
parameters = {"quick_repaying" : True,
              "diversify_trade" : True,
              "too_big_to_fail" : False, # (This one is useless in a regular grid)
              "panic_collection": True}  

## Build a network 
#network = gn.barabasi_albert_network(1000, 100, -4, -6)

#network = gn.mean_field_network(1000, -4, -6)
#pickle.dump(network, open("MEAN_FIELD_SAVED\mean_field_N1000_tl-4_ts-6.pickle", 'wb'))
network = pickle.load(open("MEAN_FIELD_SAVED\mean_field_N1000_tl-4_ts-6.pickle", "rb" ))

avalanche_sizes = dn.run_simulation(network, 500, parameters, DEBUG_BOOL = True)  # TURN OFF DEBUG_BOOL FOR SPEED (BUT TURN IT ON EVERY NOW AND THEN)

## Plot the distribution of avalanches
an.histogram_avalanches(avalanche_sizes, num_bins = 100, y_scale='log', x_scale='linear')
an.histogram_avalanches(avalanche_sizes, num_bins = 100, y_scale='log', x_scale='log')