# -*- coding: utf-8 -*-
""" ===========================================================================
This script is where we adjust parameters and run the model
=========================================================================== """
import generate_network as gn
import dynamics_network as dn
import analyze_network as an
import networkx as nx
import pickle
import numpy as np
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
              "infections_on": True}

avalanche_sizes = []

BALANCES = [0, 1, 2, 3]
BALANCE_mean = []
BALANCE_sd = []
for B in BALANCES:
    parameters['BALANCE'] = B
    for i in range(100):  # 100 simulations
        network = pickle.load(open("MEAN_FIELD_SAVED\mean_field_N100_tl-2_ts-40.pickle", "rb" ))
        network.graph['Tl'] = -2
        network.graph['Ts'] = -40
        # Each sim outputs a list of avalanche sizes
        avalanche_sizes.append(dn.run_simulation(network, 1000, parameters, DEBUG_BOOL = False))
    total_default_list = [sum(lst)/len(network.nodes()) for lst in avalanche_sizes]
    BALANCE_mean.append(np.mean(total_default_list))
    BALANCE_sd.append(np.std(total_default_list))

plt.errorbar(BALANCES, BALANCE_mean, BALANCE_sd)
plt.show()
