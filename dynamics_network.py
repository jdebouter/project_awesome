# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we implement the dynamical rules governing the
interaction between nodes and the evolution of the network

Note: I'm not sure if this partitioning makes sense, we can change it
as we go along of course.

NOTE: Right now, if a node has positive liquidity it will prioritize investing
in neighbors with the least amount of negative negativity for the following
reasons: this bank is the easiest to balance out, and thus it is the
safest bet for the bank with positive liquidity. For this bank it's most
likely that it won't lose its investment.

Also, if it has several debts, it will repay the large debts back first,
where the rationale is that large debts would have large interest payments,
so there's more incentive to repay those



=========================================================================== """

import networkx as nx
import random
import operator

''' Run the simulation for T iterations '''
def run_simulation(network, T):
    avalanches = []  # list of the sizes of all avalanches
    
    # Simulation kernel
    for t in range(T):
        # Generate random perturbations in the liquidity for each node
        _perturbate(network)
        
        # Banks trade liquidity amongst each other
        _trade(network)
        
        # Check for bankruptcy and spread infection
#        _checkAndSpreadInfection(network, avalanches)
        
        # After propagation of the avalanche is complete, reset any banks to new, balanced banks
        _resetBankruptBanks(network)
                    
    # Return the list of avalanche sizes
    return avalanches

''' Each bank gets or loses some capital randomly (delta=1 v delta=-1) '''
def _perturbate(network):
    for node in network.nodes_iter(data=True):  # data=True makes it retrieve all extra attributes
        # Randomly generate delta    
        delta = random.choice([-1, 1])
        # [1] gets the node-associated dictionary with attributes    
        node[1]['capital'] += delta
        node[1]['liquidity'] += delta

''' Trading of liquidity - UNFINISHED'''
def _trade(network):
        for node in network.nodes_iter(data=True):
            if node[1]['liquidity'] > 0:
                # If this node has some local money lying around, prioritize paying debts
                in_debt, loaners = _determine_if_in_debt(network, node[0])  # loaners is a dict with names as keys and loans as values
                if in_debt:
                    # Repay as much as possible to the loaner associated with the highest current debt
                    while node[1]['liquidity'] > 0:
                        # If the debt to that loaner is more than my liquidity, just give it all
                        max_loaner = max(loaners, key=loaners.get)
                                                    # If the debt is completely repaid, set the borrower/loaner to None
                            if our_edge[2]['debt'] == 0:
                                our_edge[2]['borrower'] = None
                                our_edge[2]['loaner'] = None
                        if loaners[max_loaner] > node[1]['liquidity']:
                            network.node[max_loaner][debt] -= node[1]['liquidity']
                            node[1]['liquidity'] = 0
                            # Update the associated edge
                            our_edge = network.edge[node[0]][max_loaner]
                            our_edge[2]['debt'] -= node[1]['liquidity']
                        else:
                        
                        
                        # Decrement my liquidity, increment liquidity of first loaner
                        # if we're at the last loaner, and its associated debt == 0, break from this loop
                        
                # Make a list of neighbors with shortfall / negative local unbalanced money / negative liquidity to invest in
                # NOTE: broke_neighbors is a list of names
                my_neighbors = network.neighbors(node[0])
                broke_neighbors = [n for n in my_neighbors if network.node[n]['liquidity'] < 0]
                neighbor_index = 0  # This index is used to iterate through the list 
                while node[1]['liquidity'] > 0 and len(broke_neighbors) > 0:
                    node[1]['liquidity'] -= 1
                    network.node[broke_neighbors[0]]['liquidity'] += 1
                    # Depending on whether there is already a loan, update the edge appropriately
                    our_edge = network.edge[node[0]][broke_neighbors[0]]
                    if our_edge['debt'] == 0:
                        our_edge['borrower'] = broke_neighbors[0]
                        our_edge['loaner'] = node[0]
                        our_edge['debt'] = 1
                    elif our_edge['debt'] != 0 and our_edge['loaner'] == node[0]:
                        our_edge['debt'] += 1
                    elif our_edge['debt'] == 1 and our_edge['borrower'] == node[0]:
                        pass
    
''' Check for bankrupty and spread infections '''
def _checkAndSpreadInfection(network, avalanches):
    a_bank_is_bankrupt = False  # Is any bank bankrupt?
    bankrupt_banks = []  # list of names currently bankrupt banks (used during avalanche propagation)
    
    # Is any bank bankrupt?
    a_bank_is_bankrupt, bankrupt_banks = _find_bankruptcies(network)
    if a_bank_is_bankrupt:  # A new avalanche has started, record it
        avalanches.append(0)
            
    # While any bank is bankrupt, propagate the failure avalanche
    while a_bank_is_bankrupt:
        for node in bankrupt_banks:
            # Make list of neighbors that loaned this bank money (we call them 'infected')
            infected = []
            my_edges = network.edges([node[0]], data=True)
            for edge in my_edges:
                if edge[2]['debt'] > 0 and edge[2]['borrower'] == node[0]:  # If this node borrowed from someone
                    infected.append(edge[2]['loaner'])  # Add that someone to the infected
                    
            # For each 'infected' neighbor, have them try to get their lost money back
            for node in infected:
                pass  # UNFINISHED
            
        # See if any more banks are bankrupt
        a_bank_is_bankrupt, bankrupt_banks = _find_bankruptcies(network)
        
        # Increment the current avalanche
        avalanches[-1] += 1

''' After infections and avalance is done, reset bankrupt banks to balanced bankss '''
def _resetBankruptBanks(network):
    for node in network.nodes_iter(data=True):  
        if node[1]['bankrupt']:
            # Reset the capital
            node[1]['capital'] = 0
            node[1]['liquidity'] = 0
            # Reset the associated edges. NOTE: node[0] is the NAME of this node (in string format)
            for edge in network.edges([node[0]]):
                network[edge[0]][edge[1]]['debt'] = 0  # network[node1][node2] gives the associated edge. This way of modifying the edge seems contrived and like it could be done easier, but I read that modifying the edge directly is a bad idea here: http://networkx.readthedocs.io/en/networkx-1.11/tutorial/tutorial.html#accessing-edges
                network[edge[0]][edge[1]]['loaner'] = None
                network[edge[0]][edge[1]]['borrower'] = None
            # no longer bankrupt
            node[1]['bankrupt'] = False

    
''' helper function for determining if a given node has a debt. '''
def _determine_if_in_debt(network, node_name):
    in_debt = False
    loaners = {}
    my_edges = network.edges([node_name], data=True)
    for edge in my_edges:
        if edge[2]['debt'] != 0 and edge[2]['borrower'] == node_name:
            in_debt = True
            loaners[edge[2]['loaner']] = edge[2]['debt']
    return in_debt, loaners

''' helper function for checking if any banks are now bankrupt '''           
def _find_bankruptcies(network):
    a_bank_is_bankrupt = False
    bankrupt_banks = []
    for node in network.nodes_iter(data=True):
        # Check whether this node is bankrupt
        if node[1]['capital'] <= network.graph['Ts'] or node[1]['liquidity'] <= network.graph['Tl']:
            # If this node is already set to bankrupt, then we've already considered it during avalanche propagation.
            if not node[1]['bankrupt']:
                node[1]['bankrupt'] = True
                bankrupt_banks.append(node)
                a_bank_is_bankrupt = True
    return a_bank_is_bankrupt, bankrupt_banks