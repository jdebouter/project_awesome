# -*- coding: utf-8 -*-
""" ===========================================================================
This script is where we adjust parameters and run the model
=========================================================================== """
import generate_network as gn
import dynamics_network as dn
import analyze_network as an
import networkx as nx

## Build a network 
network = gn.regular_network(L = 100, d = 2, Tl = -4, Ts = -6)

''' Parameters that change the implementation a little:
    quick_repaying = True/False. True means that banks will repay a debt if 
        that happen to get a surplus that round, even if they have negative 
        liquidity. False means that they'll only repay if they have positive 
        capital/liquidity 
    transfer_pattern - node_by_node/evenly_distributed. 'node_by_node' means
        that some random node is chosen and all debt/loan is repayed / collected
        until balance is regained. 'evenly_distributed' means that they'll try
        to repay/collect from all borrowers/lenders evenly
    loan_initiator = surplus/deficit. 'surplus' means that nodes with extra
        capital/liqiudity will look for broke neighbors to extend loans.
        'deficit' means that nodes with negative capital/liquidity will look
        for rich neighbors to ask for loans
    infection_collect = all/lost_money. 'all' means that nodes collect all 
        loans back after infection. 'lost_money' means that they only collect
        back any money that was lost. '''
parameters = {"quick_repaying" : False,
              "transfer_pattern" : "node_by_node",
              "loan_initiator" : "surplus",
              "infection_collect" : "all"}

#avalanche_sizes = dn.run_simulation(network, 20)

## Plot the distribution of avalanches
for i in range(10):
    print(i)
    network = gn.regular_network(L = 100, d = 2, Tl = -4, Ts = -6)

    avalanche_sizes = dn.run_simulation(network, 1000)
    for ava in avalanche_sizes:
        avalanches.append(ava)

an.histogram_avalanches(avalanche_sizes, num_bins = 1000, y_scale='log', x_scale='linear')