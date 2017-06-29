# -*- coding: utf-8 -*-
""" ===========================================================================
This script is where we adjust parameters and run the model
=========================================================================== """
import sys
sys.path.insert(0, '/Users/Jed/GitHub/project_awesome')
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
              "panic_mode": True,
              "BALANCE" : 0,
              "DELTA" : 1,
              "panic_reduced" : False,
              "infections_on": True}

PARAMETER = 'BALANCE'
#PARAMETER_VALUES = [0, 3]
PARAMETER_VALUES =  [0, 1, 2, 3]

avalanche_sizes_all_parameters = []

MEANS = []
STD_DEVIATIONS = []
m_means = []
m_errors = []
c_means = []
c_errors = []

for param in PARAMETER_VALUES:
    # Avalanche_sizes is a list of lists, the sublists contain the avalanche sizes for an individual run
    avalanche_sizes = []
    m_vals = []
    c_vals = []
    parameters[PARAMETER] = param
    for i in range(50):
        # network = pickle.load(open("../MEAN_FIELD_SAVED/mean_field_N100_tl-2_ts-40.pickle", "rb" ))
        network = pickle.load(open("../MEAN_FIELD_SAVED/mean_field_N100_tl-2_ts-40.pickle", "rb" ))
        network.graph['Tl'] = -2
        network.graph['Ts'] = -40
        # Each sim outputs a list of avalanche sizes
        results = dn.run_simulation(network, 1000, parameters, DEBUG_BOOL = False)
        # print (results)
        avalanche_sizes.append(results)
    flatten = np.array([val for sublist in avalanche_sizes for val in sublist])
    m, c, m_error, c_error = an.plot_avalanches(flatten, label='_', color='k', num_bins = 100)
        # m_vals += [m]
        # c_vals += [c]
    # Total_default_list is a list of single statistics per run, the total number of defaults
    total_default_list = [sum(lst)/len(network.nodes()) for lst in avalanche_sizes]

    # m_means.append(np.mean(m_vals))
    # m_errors.append(1.96 * np.std(m_vals) / np.sqrt(len(m_vals)) )
    # c_means.append(np.mean(c_vals))
    # c_errors.append(1.96 * np.std(c_vals) / np.sqrt(len(c_vals)) )

    m_means.append(m)
    m_errors.append(m_error)
    c_means.append(c)
    c_errors.append(c_error)

    avalanche_sizes_all_parameters.append(avalanche_sizes)
    # MEANS is a list containing the average of the total # of defaults, for all different parameter values (eg balance 0, 1, 2 ,3)
    MEANS.append(np.mean(total_default_list))
    STD_DEVIATIONS.append(1.96 * np.std(total_default_list) / np.sqrt(len(total_default_list)) )

plt.figure(1)
h1 = avalanche_sizes_all_parameters[0]
h2 = avalanche_sizes_all_parameters[-1]
f1 = np.array([val for sublist in h1 for val in sublist])
f2 = np.array([val for sublist in h2 for val in sublist])
an.plot_avalanches(f1, label='balance=0', color='b', token='*', num_bins = 100, plot=True)
an.plot_avalanches(f2, label='balance=3', color='g', token='>', num_bins = 100, plot=True)
plt.xlabel('Avalanche Sizes')
plt.ylabel('Frequency')
plt.legend()
# plt.show()

plt.figure('default size')
# PLOT TOTAL DEFAULT MEANS WITH CONFIDENCE INTERAVLS
an.confidencePlot(PARAMETER_VALUES, MEANS, STD_DEVIATIONS)

plt.figure('slope')
# PLOT TOTAL DEFAULT MEANS WITH CONFIDENCE INTERAVLS
an.confidencePlot(PARAMETER_VALUES, m_means, m_errors)

plt.figure('intercept')
# PLOT TOTAL DEFAULT MEANS WITH CONFIDENCE INTERAVLS
an.confidencePlot(PARAMETER_VALUES, c_means, c_errors)
plt.show()
