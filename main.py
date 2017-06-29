# -*- coding: utf-8 -*-
""" ===========================================================================
This script is where we adjust parameters and run the model
=========================================================================== """
import generate_network as gn
import dynamics_network as dn
import analyze_network as an
import networkx as nx
import pickle
import matplotlib.pyplot as plt

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
              "too_big_to_spread": False,
              "panic_collection": True,
              "BALANCE" : 0,
              "infections_on": True,
              "scale": 1}

#pickle.dump(network, open("MEAN_FIELD_SAVED\mean_field_N100_tl-2_ts-40.pickle", 'wb'))
network = pickle.load(open("MEAN_FIELD_SAVED/mean_field_N100_tl-2_ts-40.pickle", "rb" ))
network.graph['hubs'] = dn._find_hubs(network)

# print("hubs: %i" % len(network.graph['hubs']))

# avalanche_sizes, avalanche_sizes2 = [], []

for i in range(1):
    network = pickle.load(open("MEAN_FIELD_SAVED/mean_field_N100_tl-2_ts-40.pickle", "rb" ))
# #    network = gn.mean_field_network(4, -2, -40)
    network.graph['Tl'] = -2
    network.graph['Ts'] = -40
    # parameters['too_big_to_spread'] = False
# #    parameters['infections_on'] = False    
    # parameters['BALANCE'] = 0
    # # parameters['scale'] = 1
    
    avalanche_sizes = dn.run_simulation(network, 500, parameters, DEBUG_BOOL = False)  # TURN OFF DEBUG_BOOL FOR SPEED (BUT TURN IT ON EVERY NOW AND THEN)
    an.plot_avalanches(avalanche_sizes, label='he', color='k', num_bins = 100)
    # print(an.fit_line(range(len(avalanche_sizes)), avalanche_sizes))
    
    # network = pickle.load(open("MEAN_FIELD_SAVED/mean_field_N100_tl-2_ts-40.pickle", "rb" ))
# #    network = gn.mean_field_network(4, -2, -40)
    # network.graph['Tl'] = -1
    # network.graph['Ts'] = -40
    # parameters['too_big_to_spread'] = True
# #    parameters['no_infections'] = False
   # # parameters['less_risk'] = True
    # parameters['BALANCE'] = 1
    # # parameters['scale'] = .75
    
    # #avalanche_sizes2 = None
    # avalanche_sizes2 += dn.run_simulation(network, 1000, parameters, DEBUG_BOOL = False)  # TURN OFF DEBUG_BOOL FOR SPEED (BUT TURN IT ON EVERY NOW AND THEN)

# ### Plot the distribution of avalanches
# an.histogram_avalanches(avalanche_sizes, avalanche_sizes2, num_bins = 100, x_scale='linear',labels = ["False", "True"])
# an.histogram_avalanches(avalanche_sizes, avalanche_sizes2, num_bins = 100, x_scale='log', labels = ["Infections on", "Infections off"])
# m = an.plot_with_line(avalanche_sizes, label='scale = 1', color='g', cutoff = 0, num_bins = 50, plot=True)
# print(m)
# m = an.plot_with_line(avalanche_sizes2, label='scale = .75', color='b', cutoff = 0, num_bins = 50, plot=True)
# print(m)
# an.histogram_avalanches(avalanche_sizes, avalanche_sizes2, num_bins = 100, x_scale='log', labels = ["Infections on", "Infections off"])
# plt.legend()


# plt.show()
