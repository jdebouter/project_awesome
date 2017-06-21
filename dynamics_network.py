# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we implement the dynamical rules governing the
interaction between nodes and the evolution of the network

NOTE: Right now, if a node has positive liquidity it will prioritize investing
in neighbors with the least amount of negative liquidity for the following
reasons: this bank is the easiest to balance out, and thus it is the
safest bet for the bank with positive liquidity. For this bank it's most
likely that it won't lose its investment.

Also, if it has several debts, it will repay the large debts back first,
where the rationale is that large debts would have large interest payments,
so there's more incentive to repay those

NOTE FOR UNDERSTANDING SYNTAX:
nodes look like this: 
    (name, {'capital': 0, 'liquidity': 0, 'bankrupt': False})
edges like this: 
    (name1, name2, {'debt': 0, 'lender': None, 'borrower': None})
    
For a given node n and edge e, n[0] gives its name and n[1] gives
the associated dictionary with extra attributes. e[0] and e[1] give the names
of the associated nodes, while e[2] gives the dictionary with extra attributes.
It should also be noted that these names DON'T have to be strings. In fact,
for the lattice/regular network they're tuples of integers, eg (0,1)

Note: not sure if this is important, because I'm not sure if this situation
ever arises: if a bank fails while it has a loan extended to a neighbor, 
that neighbor's capital/liquidity should just increase by that loan I think
(and the edge should be cleared). Right now this is not implemented as I'm
assuming this situation never arises, because banks that fail have already
recovered any debts
=========================================================================== """

import networkx as nx
import random

''' Run the simulation for T iterations '''
def run_simulation(network, T):
    avalanche_sizes = []  # list of the sizes of all avalanches
    
    # Simulation kernel
    for t in range(T):
        # Generate random perturbations in the liquidity for each node
        _perturb(network)
        
        # Banks with surplus liquidity try to repay debts
        _repay_debts(network)
        
        # Banks with surplus liquidity try to invest in neighbors with negative liquidity
        _invest_surplus_liquidity(network)
        
        # Check for bankruptcy and propagate infection/failures. If an avalanche happens, its size is appended to avalanche_sizes
        _check_and_propagate_avalanche(network)
                    
    # Return the list of avalanche sizes
    return avalanche_sizes

''' Each bank gets or loses some capital randomly (delta=1 v delta=-1) '''
def _perturb(network):
    for node in network.nodes_iter(data=True):  # data=True makes it retrieve all extra attributes
        # Randomly generate delta    
        delta = random.choice([-1, 1])
        # Update liquidity and capital
        node[1]['capital'] += delta  # [1] gets the node-associated dictionary with attributes    
        node[1]['liquidity'] += delta

''' Banks with surplus liquidity repay debts  '''
def _repay_debts(network):
    for node in network.nodes_iter(data=True):
        if node[1]['liquidity'] > 0:
            # Determine if this node is in debt, and to whom
            in_debt, lenders = __find_lenders(network, node[0])  # lenders is a dict with names as keys and loansizes as values
            if in_debt:
                # Repay as much as possible to the lender associated with the highest current debt
                while node[1]['liquidity'] > 0:
                    max_lender = max(lenders, key=lenders.get)
                    our_edge = network.edge[node[0]][max_lender]
                    # If the debt to that lender is more than (or equal to) my liquidity, just give it all
                    if lenders[max_lender] >= node[1]['liquidity']:
                        # Add to lenders liquidity
                        network.node[max_lender]['liquidity'] += node[1]['liquidity']
                        # Update the associated edge
                        our_edge['debt'] -= node[1]['liquidity']
                        if our_edge['debt'] == 0:  # Reset the borrower/lender attributes if the debt is payed now
                            our_edge['borrower'] = None
                            our_edge['lender'] = None
                        # Subtract from my liquidity
                        node[1]['liquidity'] = 0
                    # Else pay off the debt and move on to the next lender
                    else:
                        # Add to lenders liquidity
                        network.node[max_lender]['liquidity'] += our_edge['debt']
                        # Subtract from my liquidity
                        node[1]['liquidity'] -= our_edge['debt']
                        # Update the associated edge
                        our_edge['debt'] = 0
                        our_edge['borrower'] = None
                        our_edge['lender'] = None
                        # move on to next lender because there is liquidity left, or STOP if no lenders are left
                        lenders.pop(max_lender)
                        if len(lenders) == 0:
                            break

''' Banks with surplus liquidity try to invest in neighbors with negative liquidity '''
def _invest_surplus_liquidity(network):
    for node in network.nodes_iter(data=True):        
        # If there's still liquidity left, help out any broke neighbors
        if node[1]['liquidity'] > 0:
            # Make a list of neighbors with negative liquidity to invest in
            have_broke_neighbors, broke_neighbors = __find_broke_neighbors(network, node[0])  # NOTE: broke_neighbors is a dict with names as keys and negative liquidities as (negative) values
            if have_broke_neighbors:
                # Invest money in neighbor with least imbalance / highest liquidity
                while node[1]['liquidity'] > 0:
                    least_broke = max(broke_neighbors, key=broke_neighbors.get)
                    our_edge = network.edge[node[0]][least_broke]
                    # If we don't have enough (or exactly enough) liquidity to restore this neighbor to balance, just give it all
                    if node[1]['liquidity'] <= -broke_neighbors[least_broke]:
                        # Add to broke neighbor's liquidity
                        network.node[least_broke]['liquidity'] += node[1]['liquidity']
                        # Update associated edge
                        our_edge['debt'] += node[1]['liquidity']
                        our_edge['borrower'] = least_broke
                        our_edge['lender'] = node[0]
                        # Subtract from my liquidity
                        node[1]['liquidity'] = 0
                    # else we have more liquidity than needed to restore this neighbor to balance, so do it and move on
                    else:                        
                        # Subtract from my liquidity
                        node[1]['liquidity'] += broke_neighbors[least_broke]
                        # Update associated edge
                        our_edge['debt'] += -broke_neighbors[least_broke]
                        our_edge['borrower'] = least_broke
                        our_edge['lender'] = node[0]
                        # Add to broke neighbor's liquidity
                        network.node[least_broke]['liquidity'] = 0
                        # Move on to next neighbor with negative liquidity, or STOP if there's none left
                        broke_neighbors.pop(least_broke)
                        if len(broke_neighbors) == 0:
                            break
    
''' UNTESTED. Check for bankrupty and spread infections. Note, I'm calling it 
    avalanche now to distinguish between:
    - avalanche: cascade of failures
    - infection: cascade of banks trying to regain balance by asking money from borrowers '''
def _check_and_propagate_avalanche(network):
    # If any bank has gone bankrupt, start an infection. Also get a list of bankrupt banks
    infection_spreading, bankrupt_banks = __find_bankruptcies(network)  # list of bankrupt banks is a list of names
    current_infected = []  # infected is a list of names
    
    while infection_spreading:
        # For each bankrupt bank, determine if any of their neighbors are infected, and how much capital they lost  
        for bankrupt_bank in bankrupt_banks:
            for neighbor in network.neighbors(bankrupt_bank):
                our_edge = network.edge[bankrupt_bank][neighbor]
                # If there is a debt, and the neighbor was the lender, add this neighbor to the infected
                if our_edge['debt'] != 0 and our_edge['lender'] == neighbor:
                    current_infected.append(neighbor)
                    # Remove the loaned money from the infected neighbor's capital
                    network.node[neighbor]['capital'] -= our_edge['debt']
                    # Reset the edge
                    __reset_edge(our_edge)

        # For each of the infected, try to recover losses
        new_infected = []
        for node in current_infected:
            for neighbor in network.neighbors(node):
                our_edge = network.edge[node][neighbor]
                # If the infected node loaned money to this neighbor
                if our_edge['debt'] != 0 and our_edge['lender'] == node:
                    # recover that money
                    network.node[node]['liquidity'] += our_edge['debt']
                    # Subtract from the neighbor
                    network.node[neighbor]['liquidity'] -= our_edge['debt']
                    # Reset the edge
                    __reset_edge(our_edge)
                    # Add the neighbor to newly infected
                    new_infected.append(neighbor)

        # Reset currently bankrupt banks. Check for any new bankruptcies
        _reset_bankrupt_banks(network)  # NOTE: this function now iterates through the entire network when it could just be passed bankrupt_banks. Fix/optimize this later
        a_bank_is_bankrupt, bankrupt_banks = __find_bankruptcies(network)
        
        # Evaluate if the infection spreading is finished or not
        infection_spreading = False
        if a_bank_is_bankrupt or len(new_infected) != 0:
            infection_spreading = True
            current_infected = new_infected




''' =========================================================================== 
HELPER FUNCTIONS
=========================================================================== '''

''' Helper function for resetting an edge '''
def __reset_edge(edge):
    edge['debt'] = 0
    edge['borrower'] = None
    edge['lender'] = None

''' Helper function for determining if a given node has a debt. Returns 
    True/False and returns a dict with all nodes who loaned money to the given 
    node, and how much. '''
def __find_lenders(network, node_name):
    in_debt = False
    lenders = {}
    my_edges = network.edges_iter([node_name], data=True)
    for edge in my_edges:
        # Does this edge have a debt where the given node is the borrower?
        debt = edge[2]['debt']
        if debt != 0 and edge[2]['borrower'] == node_name:
            # Then return true and add the lender to output
            in_debt = True
            lenders[edge[2]['lender']] = edge[2]['debt']
    return in_debt, lenders

''' Helper function for determining if a given node has neighbors with negative
    liquidity. Returns True/False, and a dict with the broke neighbors and 
    the values of their negative liquidities. '''
def __find_broke_neighbors(network, node_name):
    have_broke_neighbors = False
    broke_neighbors = {}
    my_neighbors = network.neighbors(node_name)
    for n in my_neighbors:
        # Does any neighbor have negative liquidity?
        liquidity = network.node[n]['liquidity']
        if liquidity < 0:
            # Then return true and add it to the output
            have_broke_neighbors = True
            broke_neighbors[n] = liquidity
    return have_broke_neighbors, broke_neighbors

''' Helper function for checking if any banks are now bankrupt '''           
def __find_bankruptcies(network):
    a_bank_is_bankrupt = False
    bankrupt_banks = []
    for node in network.nodes_iter(data=True):
        # Check whether this node is bankrupt
        if node[1]['capital'] <= network.graph['Ts'] or node[1]['liquidity'] <= network.graph['Tl']:
            node[1]['bankrupt'] = True
            bankrupt_banks.append(node[0])
            a_bank_is_bankrupt = True
    return a_bank_is_bankrupt, bankrupt_banks

''' Helper function for resetting all bankrupt banks '''
def _reset_bankrupt_banks(network):
    for node in network.nodes_iter(data=True):  
        if node[1]['bankrupt']:
            # Reset the capital
            node[1]['capital'] = 0
            node[1]['liquidity'] = 0
            # Reset the associated edges. NOTE: node[0] is the NAME of this node (in string format)
            for edge in network.edges([node[0]]):
                network[edge[0]][edge[1]]['debt'] = 0  # network[node1][node2] gives the associated edge. This way of modifying the edge seems contrived and like it could be done easier, but I read that modifying the edge directly is a bad idea here: http://networkx.readthedocs.io/en/networkx-1.11/tutorial/tutorial.html#accessing-edges
                network[edge[0]][edge[1]]['lender'] = None
                network[edge[0]][edge[1]]['borrower'] = None
            # no longer bankrupt
            node[1]['bankrupt'] = False