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

NOTE: I think this could be a difference between my implementation and the
article: when infected nodes lose capital due to a neighboring node failing,
they proceed to recover ALL loaned money. I felt like this is what the 
article implied in the rule section, in the 5th bullet point. However,
I could imagine they only recover the amount of loaned money they lost, 
which would reduce the amount of avalanches I think. Maybe that's how they 
implemented it?

=========================================================================== """

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
        
        # Banks without surplus but can collect money back
        _collect_loans(network)
        
        # Banks with surplus liquidity try to invest in neighbors with negative liquidity
        _invest_surplus_liquidity(network)
        
        # Check for bankruptcy and propagate infection/failures. If an avalanche happens, its size is appended to avalanche_sizes
        _check_and_propagate_avalanche(network, avalanche_sizes)
                    
    # Return the list of avalanche sizes
    return avalanche_sizes

''' Each bank gets or loses some capital randomly (delta=1 v delta=-1) '''
def _perturb(network):
    for node in network.nodes():  # data=True makes it retrieve all extra attributes
        # Randomly generate delta    
        delta = random.choice([-1, 1])
        # Update liquidity and capital
        node.changeLiquidity(delta)
        node.changeCapital(delta)

''' Banks with surplus liquidity repay debts  '''
def _repay_debts(network):
    # Iterate through the node list randomly
    node_list = network.nodes()[:]
    random.shuffle(node_list)
    for node in node_list:
        # Do I have liquidity to repay debt with?
        if node.getLiquidity() > 0:
            # Determine if this node is in debt, and to whom
            node.findBorrowersLenders()
            lenders = node.getLenders()
            # Iterate through all lenders randomly to pay back debt
            for lender in lenders:
                debt = node.getDebt(lender)  # How much money do I owe this lender?
                if node.getLiquidity() >= debt:   # Do I have enough money to repay it all?
                    node.transfer(lender, debt)  # Repay it all
                else:
                    node.transfer(lender, node.getLiquidity())  # Else pay whatever I have
                    break

''' Banks with negative liquidity collects loans  '''
def _collect_loans(network):
    # Iterate through the node list randomly
    node_list = network.nodes()[:]
    random.shuffle(node_list)
    for node in node_list:
        # Do I have a deficit?
        if node.getLiquidity() < 0:
            # Determine if this if anyone owes this node money
            node.findBorrowersLenders()
            borrowers = node.borrowers
            # Iterate through all borrowers randomly to collect loans
            for borrower in borrowers:
                debt = node.getDebt(borrower)  # How much money does this borrower have to offer me?
                if abs(node.getLiquidity()) >= debt:  # If our deficit is bigger than the debt
                    borrower.transfer(node, debt)  # Take it all back
                else:
                    borrower.transfer(node, abs(node.getLiquidity()))  # Else take what is needed to regain balance
                    break

''' Banks with surplus liquidity try to invest in neighbors with negative liquidity '''
def _invest_surplus_liquidity(network):
    # Iterate through the node list randomly
    node_list = network.nodes()[:]
    random.shuffle(node_list)
    for node in node_list:        
        # If there's still liquidity left, help out any broke neighbors
        if node.getLiquidity() > 0:
            node.findBrokeNeighbours()
            broke_neighbours = node.getBrokeNeighbours()
            # Iterate through broke neighbors to invest in
            for broke in broke_neighbours:
                money_needed = -broke.getLiquidity()  # How much money does this neighbor need?
                if node.getLiquidity() >= money_needed:  # Do I have enough money for that?
                    node.transfer(broke, money_needed)  # Transfer that amount
                else:
                    node.transfer(broke, node.getLiquidity())  # Else transfer what I have
                    break
    
''' Check for bankrupty and spread infections. Note, I'm calling it 
    avalanche now to distinguish between:
    - avalanche: cascade of failures
    - infection: cascade of banks trying to regain balance by asking money from borrowers '''
def _check_and_propagate_avalanche(network, avalanche_sizes):
    # If any bank has gone bankrupt, start an infection. Also get a list of bankrupt banks
    bankrupt_banks = __find_bankruptcies(network)  # list of bankrupt banks is a list of names
    for banks in bankrupt_banks:
        pass
        
        
                                        
                                        
#    current_infected = []  # infected is a list of names
#    
#    # Start recording this avalanche
#    if infection_spreading:
#       avalanche_sizes.append(len(bankrupt_banks)) 
#    
#    while infection_spreading:
#        # For each bankrupt bank, determine if any of their neighbors are infected, and how much capital they lost  
#        for bankrupt_bank in bankrupt_banks:
#            for neighbor in network.neighbors(bankrupt_bank):
#                our_edge = network.edge[bankrupt_bank][neighbor]
#                # If there is a debt, and the neighbor was the lender, add this neighbor to the infected
#                if our_edge['debt'] != 0 and our_edge['lender'] == neighbor:
#                    current_infected.append(neighbor)
#                    # Remove the loaned money from the infected neighbor's capital
#                    network.node[neighbor]['capital'] -= our_edge['debt']
#                    # Reset the edge
#                    __reset_edge(our_edge)
#
#        # For each of the infected, try to recover losses
#        new_infected = []
#        for node in current_infected:
#            for neighbor in network.neighbors(node):
#                our_edge = network.edge[node][neighbor]
#                # If the infected node loaned money to this neighbor
#                if our_edge['debt'] != 0 and our_edge['lender'] == node:
#                    # recover that money
#                    network.node[node]['liquidity'] += our_edge['debt']
#                    # Subtract from the neighbor
#                    network.node[neighbor]['liquidity'] -= our_edge['debt']
#                    # Reset the edge
#                    __reset_edge(our_edge)
#                    # Add the neighbor to newly infected
#                    new_infected.append(neighbor)
#
#        # Reset currently bankrupt banks. Check for any new bankruptcies
#        _reset_bankrupt_banks(network)  # NOTE: this function now iterates through the entire network when it could just be passed bankrupt_banks. Fix/optimize this later
#        a_bank_is_bankrupt, bankrupt_banks = __find_bankruptcies(network)
#        
#        # record avalanche
#        avalanche_sizes[-1] += len(bankrupt_banks)
#        
#        # Evaluate if the infection spreading is finished or not
#        infection_spreading = False
#        if a_bank_is_bankrupt or len(new_infected) != 0:
#            infection_spreading = True
#            current_infected = new_infected




''' =========================================================================== 
HELPER FUNCTIONS
=========================================================================== '''



''' Helper function for checking if any banks are now bankrupt '''           
def __find_bankruptcies(network):
    bankrupt_banks = []
    for node in network.nodes():
        # Check whether this node is bankrupt
        if node.getCapital() <= network.graph['Ts'] or node.getLiquidity() <= network.graph['Tl']:
            node.setBankruptancy(True)
            bankrupt_banks.append(node)
            
    return bankrupt_banks

''' Helper function for resetting all bankrupt banks '''
def _reset_bankrupt_banks(network):
    for node in network.nodes():  
        if node.getBankruptancy():
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