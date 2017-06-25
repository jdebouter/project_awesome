# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we implement the dynamical rules governing the
interaction between nodes and the evolution of the network

=========================================================================== """

import random
import analyze_network as an

''' Run the simulation for T iterations '''
def run_simulation(network, T, parameters = None):
    # If no parameters were input, just use the default parameters
    if parameters is None:
        parameters = default_parameters  # (defined at bottom)
    
    avalanche_sizes = []  # list of the sizes of all avalanches
    # Simulation kernel
    for t in range(T):
        if t % 10 == 0:
            print("ITERATION %i" % t)
        # Generate random perturbations in the liquidity for each node
        perturb(network)
 
        # Banks with surplus liquidity try to repay debts
        repay_debts(network)
 
        # Banks with a deficit try to collect loans back
        collect_loans(network)
  
        # Banks with surplus liquidity try to invest in neighbors with negative liquidity 
        invest_surplus_liquidity(network)
    
        # Check for bankruptcy and propagate infection/failures. If an avalanche happens, its size is appended to avalanche_sizes 
        check_and_propagate_avalanche(network, avalanche_sizes)
        
        # just checking the correctness of the program:
        debug(network)
        _debug2(network)
        
    # Return the list of avalanche sizes
    return avalanche_sizes

''' =========================================================================== 
FUNCTIONS USED IN run_simulation()
=========================================================================== '''

''' Each bank gets or loses some capital randomly (delta=1 v delta=-1) '''
def perturb(network):
    for node in network.nodes():  # data=True makes it retrieve all extra attributes
        # Randomly generate delta    
        delta = random.choice([-1, 1])
        # Update liquidity and capital
        node.changeLiquidity(delta)
        node.changeCapital(delta)

''' Banks with surplus liquidity repay debts  '''
def repay_debts(network):
    # Iterate through the node list randomly
    node_list = network.nodes()[:]
    random.shuffle(node_list)
    # Repay
    _pay_money(node_list)


''' Banks with negative liquidity collect loans  '''
def collect_loans(network):
    # Iterate through the node list randomly
    node_list = network.nodes()[:]
    random.shuffle(node_list)
    # Collect loans
    _get_money(node_list, infection_happening = False)


''' Banks with surplus liquidity try to invest in neighbors with negative liquidity '''
def invest_surplus_liquidity(network):
    # Iterate through the node list randomly
    node_list = network.nodes()[:]
    random.shuffle(node_list)
    for node in node_list:        
        # If there's still liquidity left, help out any broke neighbors
        if node.getLiquidity() > 0 and node.getCapital() > 0:  # Changed it back! The article says nodes should have positive capital, but of course you also need positive liquidity, otherwise you have nothing to loan
            # Get a list of broke neighbours        
            node.updateBrokeNeighbours()  # First update the node's list
            broke_neighbours = node.getBrokeNeighbours()
            # Iterate through broke neighbors to invest in
            for broke in broke_neighbours:
                money_needed = -broke.getLiquidity()  # How much money does this neighbor need?
                if node.getLiquidity() > money_needed:  # Do I have enough money for that?
                    node.transfer(broke, money_needed)  # Transfer that amount                    
                else:
                    node.transfer(broke, node.getLiquidity())  # Else transfer what I have                    
                    break
                
''' Check for bankrupty and spread infections. Note, I'm calling it 
    avalanche now to distinguish between:
    - avalanche: cascade of failures
    - infection: cascade of banks trying to regain balance by asking money from borrowers '''
def check_and_propagate_avalanche(network, avalanche_sizes):
    # If any bank has gone bankrupt, start an infection. Also get a list of bankrupt banks
    bankrupt_banks = _find_bankruptcies(network)  # list of bankrupt banks is a list of names

    if len(bankrupt_banks) > 0:  # If there are bankrupt banks
        
        _infect_neighbours(bankrupt_banks)  # Sets lender neighbours of bankrupt banks to infected
        infected_banks = _find_infections(network) # Put all infected banks in a list
        length_old_infections = len(infected_banks)
        
        if len(infected_banks) > 0:  # When there are infections
            while True:
                # Within one iteration, all infected nodes collect money and infect neighbors, and new bankruptcies happen
                _collect_money_and_spread_infection(infected_banks)  # Infected nodes collect money from neighbors and infect them
                bankrupt_banks = _find_bankruptcies(network)  # Find any new bankruptcies                
                _infect_neighbours(bankrupt_banks)  # Make neighbors of new bankruptcies also infected
                infected_banks = _find_infections(network)  # Make list of all currently infected
                
                # Check if there are new infections and if avalanche should be stopped
                length_new_infections = len(infected_banks) 
                if length_new_infections == length_old_infections:
                    avalanche_sizes.append(length_new_infections)
                    _cure_all(infected_banks)  # Cures infected banks
                    _reset_all(bankrupt_banks)  # resets every bank
                    break
                else:
                    length_old_infections = length_new_infections
        else:
            _reset_all(bankrupt_banks)
 
''' =========================================================================== 
HELPER FUNCTIONS
=========================================================================== '''

''' Helper function to Debug '''
def debug(network):
    for node in network.nodes():
        # if a node is a borrower and a lender, raise an exception
        borrowing, lending = False, False
        for neighbour in node.neighbours:
            if node.neighbours[neighbour] > 0:
                lending = True
            elif node.neighbours[neighbour] < 0:
                borrowing = True
        node.isCapitalRight()
        if borrowing and lending:
            raise Exception("A node is borrowing and lending at the same time. This shouldn't happen!")

''' Helper function to iterate through a given node list and retrieve loaned money from neighbours '''
def _get_money(node_list, infection_happening = False):
    for node in node_list:
        # Collect money from borrowers if I have a deficit or if an infection is happening
        if node.getLiquidity() < 0 or infection_happening:
            # Get a list of the neighbors who have borrowed money from this node
            node.updateBorrowersLenders()
            borrowers = node.getBorrowers()
            # Collect money from each
            for borrower in borrowers:
                debt = node.getDebt(borrower)  # How much has he borrowed
#                 If the debt isn't enough to cover our losses, or if this node is infected, just take it all back
                if abs(node.getLiquidity()) >= debt or infection_happening:
                    node.transfer(borrower, -debt) # 
#                    # If this node is infected, infected the borrowing neighbour too
                    if infection_happening:
                        borrower.infect()
#                # Else take only the amount back we need to regain balance (liquidity = 0)
                else:
                    node.transfer(borrower, -abs(node.getLiquidity())) 
                    if infection_happening:
                        borrower.infect()
                    break

''' Helper function to iterate through a given node list and pay back debt to neighbours'''
def _pay_money(node_list):
    for node in node_list:
        # Repay debt to lenders if I have a surplus
        if node.getLiquidity() > 0:
            # Get a list of the neighbors who have loaned money to this node
            node.updateBorrowersLenders()
            lenders = node.getLenders()
            if len(lenders) > 0:
                # Repay as much as possible to the lender associated with the highest current debt
                for lender in lenders:
                    debt = node.getDebt(lender)  # How much money do I owe?
                    if node.getLiquidity() >= debt:  # Do I have enough money to pay it back?
                        node.transfer(lender, debt)  # Pay it all back
                    else:
                        node.transfer(lender, node.getLiquidity())  # If I can't pay everything back, just give back what I have
                        break

''' =========================================================================== 
AVALANCHE RELATED HELPER FUNCTIONS
=========================================================================== '''

''' Helper function for checking if any banks are now bankrupt '''           
def _find_bankruptcies(network):
    bankrupt_banks = []
    for node in network.nodes():
        # Check whether this node is bankrupt
        if node.getCapital() <= network.graph['Ts'] or node.getLiquidity() <= network.graph['Tl']:
            node.setBankruptcy(True)
            bankrupt_banks.append(node)
#            print "hello", node.getCapital(), node.getLiquidity() 
    return bankrupt_banks

'''Helper function for creating infections'''
def _infect_neighbours(bankrupt_banks):
    
    for bank in bankrupt_banks:
        bank.updateBorrowersLenders()
        lenders = bank.getLenders()
#        _debug2(network)
#        print "hello", bank.getTotalDebt()
        for lender in lenders:
            lender.infect(bank)

'''Helper function to find infections'''
def _find_infections(network):
    infected_banks = []
    for bank in network.nodes():
        if bank.getInfection() and not bank.getBankruptcy():
            infected_banks.append(bank)
    return infected_banks

'''Helper function to cure infections'''
def _collect_money_and_spread_infection(infected_banks):
    _get_money(infected_banks, infection_happening = True)
#    _pay_money(infected_banks)
                    
'''Helper function to cure Banks'''
def _cure_all(banks):
    for bank in banks:
        bank.cure()

''' Helper function for resetting banks '''
def _reset_all(banks):
    for bank in banks:
        bank.reset()

def _debug2(network):
    for node in network.nodes():
        node.lenderBorrowerSame()
        
''' Default dictionary of parameters which vary the implementation details '''
default_parameters = \
    {"quick_repaying" : False, \
     "transfer_pattern" : "node_by_node", \
     "loan_initiator" : "surplus", \
     "infection_collect" : "all"}