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
    transfer_pattern - node_by_node/evenly_distributed. 'node_by_node' means
        that some random node is chosen and all debt/loan is repayed / collected
        until balance is regained. 'evenly_distributed' means that they'll try
        to repay/collect from all borrowers/lenders evenly
        back any money that was lost. 
    panic_collection - True/False. 'True' means that infected bank collects all
        money from all its borrower. 'False' means that bank only collects 
        back the lost capital
    too_big_to_fail - policy, more description later...'''
parameters = {"quick_repaying" : True,
              "diversify_trade" : True,
              "too_big_to_fail" : False,  # (This one is useless in a regular grid)
              "panic_collection": True}


parameters['sd'] = 1
parameters['repay_fraction'] = 1
network = pickle.load(open("MEAN_FIELD_SAVED\mean_field_N100_tl-4_ts-6.pickle", "rb" ))
network.graph['hubs'] = dn._find_hubs(network)
print("hubs: %i" % len(network.graph['hubs']))

avalanche_sizes, avalanche_sizes2 = [], []

for i in range(1):
    network = pickle.load(open("MEAN_FIELD_SAVED\mean_field_N100_tl-4_ts-6.pickle", "rb" ))
    network.graph['Tl'] = -6
    network.graph['Ts'] = -10
    parameters['too_big_to_fail'] = False    
    
    avalanche_sizes += dn.run_simulation(network, 1000, parameters, DEBUG_BOOL = True)  # TURN OFF DEBUG_BOOL FOR SPEED (BUT TURN IT ON EVERY NOW AND THEN)
    
    network = pickle.load(open("MEAN_FIELD_SAVED\mean_field_N100_tl-4_ts-6.pickle", "rb" ))
    network.graph['Tl'] = -6
    network.graph['Ts'] = -10
    parameters['too_big_to_fail'] = False
#    parameters['less_risk'] = True
    
    #avalanche_sizes2 = None
    avalanche_sizes2 += dn.run_simulation(network, 1000, parameters, DEBUG_BOOL = True)  # TURN OFF DEBUG_BOOL FOR SPEED (BUT TURN IT ON EVERY NOW AND THEN)

### Plot the distribution of avalanches
an.histogram_avalanches(avalanche_sizes, avalanche_sizes2, num_bins = 100, x_scale='linear', labels = [r"$without injections$", r"$with injections$"])
an.histogram_avalanches(avalanche_sizes, avalanche_sizes2, num_bins = 100, x_scale='log', labels = [r"$without injections$", r"$with injections$"])