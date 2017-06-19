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
        for node in network.nodes_iter(data=True):  # data=True makes it retrieve all extra attributes
            # Randomly generate delta    
            delta = random.choice([-1, 1])
            # [1] gets the node associated dictionary with attributes    
            node[1]['capital'] += delta
            node[1]['unbalanced'] += delta
                    
        # Invest surplus or loan to compensate loss, based on rules:
            # If current capital > 0, invest, otherwise borrow capital
            
            # After the loaning/borrowing segment, recompute the unbalanced local money
            
        # Check for bankruptcy
        if node[1]['capital'] <= network.graph['Ts'] or node[1]['unbalanced'] <= network.graph['Tl']:
            node[1]['bankrupt'] = True
            # Make list of neighbors that loaned this bank money
            ngbr_edges = 
            # For each neighbor that loaned this bank money, have them try to get their lost money back (this should propagate any potential avalanche)

#            for neighbor in [n for n in network.neighbors(node[0]) if :
                
            # Remember that we also have to record the avalanches somehow
            
        # Create new balanced banks in places of failed/bankrupt banks
        for node in network.nodes_iter(data=True):  
            if node[1]['bankrupt']:
                # Reset the capital
                node[1]['capital'] = 0
                # Reset the associated edges. NOTE: node[0] is the NAME of this node (in string format)
                for edge in network.edges([node[0]]):
                    network[edge[0]][edge[1]]['debt'] = 0  # network[node1][node2] gives the associated edge. This way of modifying the edge seems contrived and like it could be done easier, but I read that modifying the edge directly is a bad idea here: http://networkx.readthedocs.io/en/networkx-1.11/tutorial/tutorial.html#accessing-edges
                    network[edge[0]][edge[1]]['loaner'] = None
                # no longer bankrupt
                node[1]['bankrupt'] = False