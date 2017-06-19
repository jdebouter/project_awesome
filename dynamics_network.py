# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we implement the dynamical rules governing the
interaction between nodes and the evolution of the network

Note: I'm not sure if this partitioning makes sense, we can change it
as we go along of course.

=========================================================================== """

import networkx as nx
import random

''' Run the simulation for T iterations '''
def run_simulation(network, T):
    for t in range(T):
        # Each bank gets or loses some capital randomly (delta=1 v delta=-1)
        for node in network.nodes_iter(data='capital'):  # data='capital' makes it retrieve the capital attribute as well
            # [1] gets the node associated dictionary with attributes    
            node[1]['capital'] += random.choice([-1, 1])   
        

        # Invest surplus or loan to compensate loss, based on rules:
            # If current capital > 0, invest, otherwise borrow capital
            # 
            
        # Check for bankruptcy (capital <= solvency threshold or sum of loans <= liquidity threshold)
            # If there's a bankruptcy, do the appropriate things
                # alert neighboring banks, have them try to get losses back (this should propagate the avalanche)
                
            # Remember that we also have to record the avalanches somehow
            
            
        # Create new balanced banks (capital = 0) in places of failed banks
        for node in network.nodes_iter(data=True):
            if node[1]['bankrupt']:
                # Reset the capital
                node[1]['capital'] = 0
                # Reset the edges. NOTE: node[0] is the NAME of this node (in string format)
                for edge in network.edges([node[0]]):
                    network[edge[0]][edge[1]]['debt'] = 0  # network[node1][node2] gives the associated edge. This way of modifying the edge seems contrived and like it could be done easier, but I read that modifying the edge directly is a bad idea here: http://networkx.readthedocs.io/en/networkx-1.11/tutorial/tutorial.html#accessing-edges
                    network[edge[0]][edge[1]]['loaner'] = None
                # no longer bankrupt
                node[1]['bankrupt'] = False