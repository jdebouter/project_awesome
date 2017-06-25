# -*- coding: utf-8 -*-
""" ===========================================================================

This script is where we implement the dynamical rules governing the
interaction between nodes and the evolution of the network

=========================================================================== """

import random
import networkx as nx
import analyze_network as an
import numpy as np

DELTA = 1

''' Default dictionary of parameters which vary the implementation details '''
default_parameters = \
    {"quick_repaying" : True, \
     "transfer_pattern" : "node_by_node", \
     "infection_collect" : "all"}

''' Run the simulation for T iterations '''
def run_simulation(network, T, parameters = None):
    # If no parameters were input, just use the default parameters
    if parameters is None:
        parameters = default_parameters
    
    avalanche_sizes = []  # list of the sizes of all avalanches
    # Simulation kernel
    for t in range(T):
        if t % 10 == 0:
            print("ITERATION %i" % t)
        # Generate random perturbations in the liquidity for each node
        perturb(network)

        # Banks with surplus liquidity try to repay debts
        repay_debts(network, parameters)
 
        # Banks with a deficit try to collect loans back
        collect_loans(network, parameters)
  
        # Banks with surplus liquidity try to invest in neighbors with negative liquidity 
        invest_surplus_liquidity(network, parameters)
    
        # Check for bankruptcy and propagate infection/failures. If an avalanche happens, its size is appended to avalanche_sizes 
        check_and_propagate_avalanche(network, avalanche_sizes)
        
        # just checking the correctness of the program:
        debug(network)
        _debug2(network)
        
    # Return the list of avalanche sizes
    return avalanche_sizes

''' Run the simulation for 1 iteration and return the list of defaulted banks'''
def step_simulation(network, parameters = None):
    # If no parameters were input, just use the default parameters
    if parameters is None:
        parameters = default_parameters
    
    avalanche_sizes = []  # list of the sizes of all avalanches
    # Generate random perturbations in the liquidity for each node
    perturb(network)
 
    # Banks with surplus liquidity try to repay debts
    repay_debts(network, parameters)
 
    # Banks with a deficit try to collect loans back
    collect_loans(network)
  
    # Banks with surplus liquidity try to invest in neighbors with negative liquidity 
    invest_surplus_liquidity(network, parameters)
    
    # Check for bankruptcy and propagate infection/failures. If an avalanche happens, its size is appended to avalanche_sizes 
    return check_and_propagate_avalanche(network, avalanche_sizes)

''' =========================================================================== 
FUNCTIONS USED IN run_simulation()
=========================================================================== '''

''' Each bank gets or loses some capital randomly (delta=1 v delta=-1) '''
def perturb(network):
    for node in network.nodes():  # data=True makes it retrieve all extra attributes
        # Randomly generate delta    
        delta = random.choice([-DELTA, DELTA])
        # Update liquidity and capital
        node.changeLiquidity(delta)
        node.changeCapital(delta)
        # Nodes can base choices on this round's delta, so set it
        node.delta = delta
        
''' Banks with surplus liquidity repay debts  '''
def repay_debts(network, parameters):
    # Iterate through the node list randomly
    node_list = network.nodes()[:]
    random.shuffle(node_list)
    # Repay
    _pay_money(node_list, parameters)


''' Banks with negative liquidity collect loans  '''
def collect_loans(network, parameters):
    # Iterate through the node list randomly
    node_list = network.nodes()[:]
    random.shuffle(node_list)
    # Collect loans
    _get_money(node_list, parameters, infection_happening = False)


''' Banks with surplus liquidity try to invest in neighbors with negative liquidity '''
def invest_surplus_liquidity(network, parameters):
    # Iterate through the node list randomly
    node_list = network.nodes()[:]
    random.shuffle(node_list)
    for node in node_list:        
        # If there's still liquidity left, help out any broke neighbors
        if node.getLiquidity() > 0 and node.getCapital() > 0:  
            # Get a list of broke neighbours        
            node.updateBrokeNeighbours()  # First update the node's list
            broke_neighbours = node.getBrokeNeighbours()
            if parameters['transfer_pattern'] == 'node_by_node':
                # Iterate through broke neighbors to invest in
                for broke in broke_neighbours:
                    money_needed = -broke.getLiquidity()  # How much money does this neighbor need?
                    if node.getLiquidity() > money_needed:  # Do I have enough money for that?
                        node.transfer(broke, money_needed)  # Transfer that amount                    
                    else:
                        node.transfer(broke, node.getLiquidity())  # Else transfer what I have                    
                        break
            elif parameters['transfer_pattern'] == 'distributed_evenly':
                # As long as I have money, and there are broke neighbors to give money to, keep giving them all 1 money
                while node.getLiquidity() > 0 and len(broke_neighbours) > 0:
                    remove_these = []  # Remove lenders if debt is paid
                    for broke in broke_neighbours:
                        if broke.getLiquidity() < 0 and node.getLiquidity() > 0:
                            node.transfer(broke, DELTA)
                        elif broke.getLiquidity() >= 0:
                            remove_these.append(broke)
                    # Remove lenders whose debt is paid back
                    broke_neighbours = [b for b in broke_neighbours if not b in remove_these]
            else:
                raise Exception("Parameter doesn't exist. (Spelled wrong probably.)")
                
''' Check for bankrupty and spread infections. '''
def check_and_propagate_avalanche(network, avalanche_sizes):
    # If any bank has gone bankrupt, start an infection. Also get a list of bankrupt banks
    bankrupt_banks = _find_bankruptcies(network)  # list of bankrupt banks is a list of names
    complete_list_of_bankruptcies = []

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
                complete_list_of_bankruptcies.append(infected_banks)

                
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
    return np.ndarray.flatten(np.array(complete_list_of_bankruptcies))
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

def _debug2(network):
    for node in network.nodes():
        node.lenderBorrowerSame()

''' Helper function to iterate through a given node list and retrieve loaned money from neighbours '''
def _get_money(node_list, parameters, infection_happening = False):
    for node in node_list:
        # Collect money from borrowers if I have a deficit or if an infection is happening
        if node.getLiquidity() < 0 or infection_happening:
            # Get a list of the neighbors who have borrowed money from this node
            node.updateBorrowersLenders()
            borrowers = node.getBorrowers()
            # If the payment pattern is 'node_by_node', pick a random borrower and get the loan back, and continue like this
            if parameters['transfer_pattern'] == "node_by_node" or infection_happening:
                # Collect money from each 
                for borrower in borrowers:
                    debt = node.getDebt(borrower)  # How much has he borrowed
                    # If the debt isn't enough to cover our losses, or if this node is infected, just take it all back
                    if abs(node.getLiquidity()) >= debt or infection_happening:
                        node.transfer(borrower, -debt) # 
                        # If this node is infected, infected the borrowing neighbour too
                        if infection_happening:
                            borrower.infect()
                    # Else take only the amount back we need to regain balance (liquidity = 0)
                    else:
                        node.transfer(borrower, -abs(node.getLiquidity())) 
                        if infection_happening:
                            borrower.infect()
                        break
            # If the payment pattern is 'distributed_evenly', keep transferring one unit from each borrower until I'm balanced
            elif parameters['transfer_pattern'] == 'distributed_evenly':
                while node.getLiquidity() < 0 and len(borrowers) > 0:
                    remove_these = []  # Remove borrowers who have returned their debt
                    for borrower in borrowers:
                        if node.getDebt(borrower) > 0 and node.getLiquidity() < 0:
                            node.transfer(borrower, -DELTA)
                        elif node.getDebt(borrower) == 0:
                            remove_these.append(borrower)
                    # Remove borrowers whose debt is collected
                    borrowers = [b for b in borrowers if not b in remove_these]
            else:
                raise Exception("Parameter doesn't exist. (Spelled wrong probably)")

''' Helper function to iterate through a given node list and pay back debt to neighbours'''
def _pay_money(node_list, parameters):
    for node in node_list:
        # Repay debt to lenders if I have a surplus
        if node.getLiquidity() > 0:
            # Get a list of the neighbors who have loaned money to this node
            node.updateBorrowersLenders()
            lenders = node.getLenders()
            # If the payment pattern is 'node_by_node', pick a random lender and repay it all, and continue like this node-by-node
            if parameters['transfer_pattern'] == 'node_by_node':
                for lender in lenders:
                    debt = node.getDebt(lender)  # How much money do I owe?
                    if node.getLiquidity() >= debt:  # Do I have enough money to pay it back?
                        node.transfer(lender, debt)  # Pay it all back
                    else:
                        node.transfer(lender, node.getLiquidity())  # If I can't pay everything back, just give back what I have
                        break
            # If the payment pattern is 'distributed_evenly', keep transferring one unit to each lender until I'm out of money
            elif parameters['transfer_pattern'] == 'distributed_evenly':
                # As long as I have money, and there are lenders to give money to, keep giving them all 1 money
                while node.getLiquidity() > 0 and len(lenders) > 0:
                    remove_these = []  # Remove lenders if debt is paid
                    for lender in lenders:
                        if node.getDebt(lender) > 0 and node.getLiquidity() > 0:
                            node.transfer(lender, DELTA)
                        elif node.getDebt(lender) == 0:
                            remove_these.append(lender)
                    # Remove lenders whose debt is paid back
                    lenders = [l for l in lenders if not l in remove_these]
            else:
                raise Exception("Parameter doesn't exist. (Spelled wrong probably)")
        # If this node is broke, but 'quick_repaying' is on, and we got some money this round, pay back a random debt
        elif node.getLiquidity() < 0 and parameters['quick_repaying'] and node.delta > 0:
            node.updateBorrowersLenders()
            if len(node.getLenders()) > 0:
                lender = node.getLenders()[0]
                node.transfer(lender, node.delta)

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
    # Setting parameters to the dictionary below is a kind of hack to make it work during infection, when its value isn't important anyway
    _get_money(infected_banks, parameters = {"transfer_pattern":"node_by_node"}, infection_happening = True)
#    _pay_money(infected_banks)
                    
'''Helper function to cure Banks'''
def _cure_all(banks):
    for bank in banks:
        bank.cure()

''' Helper function for resetting banks '''
def _reset_all(banks):
    for bank in banks:
        bank.reset()
    
''' =========================================================================== 
TOO BIG TO FAIL
=========================================================================== '''
       
# Standard deviation of the degree
def _compute_sd_degree(network, average_degree):
    out = 0
    for node in network.nodes_iter():
        out += np.pow((network.degree(node) - average_degree), 2)
    return np.sqrt(out)

def _find_hubs(network):
    average_degree = nx.average_degree_connectivity(network)
    degree_sd = _compute_sd_degree(network, average_degree)
    hubs = []
    for node in network.nodes_iter():
        if network.degree(node) > average_degree + degree_sd:
            hubs.append(node)
    return hubs





if __name__ == '__main__':
    print("Run the main you idiot!")
