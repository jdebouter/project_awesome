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
    a_bank_is_bankrupt = False  # Is any bank bankrupt?
    bankrupt_banks = []  # list of names currently bankrupt banks (used during avalanche propagation)
    avalanches = []  # list of the sizes of all avalanches
    
    # Simulation kernel
    for t in range(T):
        # Generate random perturbations in the liquidity for each node
        _perturbate(network)
        
        # Banks trade liquidity amongst each other
        _trade(network)
        
        # Check for bankruptcy and spread infection
        _checkAndSpreadInfection(network)
        
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

''' Trading of liquidity '''
def _trade():
        # Invest surplus or borrow money to compensate loss, based on rules:
        for node in network.nodes_iter(data=True):
            if node[1]['liquidity'] > 0:
                # If this node has some local money lying around, prioritize paying debts, otherwise invest in broke neighbors
                in_debt, borrowers = _determine_if_in_debt(network, node[0]):
                    pass
                if in_debt:
                    while node[1]['liquidity']:
                        
                # Make a list of neighbors with shortfall / negative local unbalanced money. NOTE: broke_neighbors is a list of names
                my_neighbors = network.neighbors(node[0])
                broke_neighbors = [n for n in my_neighbors if network.node[n]['liquidity'] < 0]
                while node[1]['liquidity'] > 0 and len(broke_neighbors) > 0:
                    node[1]['liquidity'] -= 1
                    network.node[broke_neighbors[0]]['liquidity'] += 1
                    # Depending on whether there is already a loan, and to whom, do the appropriate thing
                    our_edge = network.edge[node[0]][broke_neighbors[0]]
                    if our_edge['debt'] == 0:
                        our_edge['borrower'] = broke_neighbors[0]
                        our_edge['loaner'] = node[0]
                        our_edge['debt'] = 1
                    elif our_edge['debt'] != 0 and our_edge['loaner'] == node[0]:
                        our_edge['debt'] += 1
                    elif our_edge['debt'] == 1 and our_edge[']
                    # Clarification: node[0] gets the name attribute of node, while broke_neighbors[0] gets the first broke neighbor from a list of names
    
''' Check for bankrupty and spread infections '''
def _checkAndSpreadInfection(network):
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
    loaners = []
    my_edges = network.edges([node_name], data=True)
    for edge in my_edges:
        if edge[2]['debt'] != 0 and edge[2]['borrower'] == node_name:
            in_debt = True
            debtors.append(edge[2]['loaner'])
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