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
              "panic_collection": True,
              "BALANCE" : 0}

#pickle.dump(network, open("MEAN_FIELD_SAVED\mean_field_N100_tl-2_ts-40.pickle", 'wb'))
network = pickle.load(open("MEAN_FIELD_SAVED\mean_field_N100_tl-2_ts-40.pickle", "rb" ))
network.graph['hubs'] = dn._find_hubs(network)
print("hubs: %i" % len(network.graph['hubs']))
hubs = network.graph['hubs']
network.graph['Tl'], network.graph['Ts'] = -2, -40

UNIT = 100
network.graph['Tl'] *= UNIT
network.graph['Ts'] *= UNIT

for i in range(300):
    dn.perturb(network)

dn.ask_for_investments(network, parameters)

an.print_node_list(hubs)

dn.check_and_propagate_avalanche(network, [], parameters)
dn.debug(network)

#an.print_node_list(hubs)

#dn._inject_hubs(network, [])
#
#an.print_node_list(hubs)