# -*- coding: utf-8 -*-
"""
Krish's script where he defines the bank object. This script
should be renamed
"""

import random 
import networkx as nx

# Definition of a Banking Node 

class Bank(object):
    def __init__(self, node, amount_inhand, amount_withothers = []):
        self.label = node
        self.capital = sum(amount_withothers) + amount_inhand
        self.liquidity = amount_inhand
        self.bankruptcy = False
        self.infection = False
        self.neighbours = {}

    ''' GET FUNCTIONS '''
    def getInfection(self):
        return self.infection
            
    def getLabel(self):
        return self.label
    
    def getLiquidity(self):
        return self.liquidity
        
    def getCapital(self):
        return self.capital
    
    def getNeighbours(self):
        return self.neighbours.keys()
    
    def getTotalDebt(self):
        return sum(self.neighbours.values())
    
    def getBankruptcy(self):
        return self.bankruptcy
    
    def getBorrowers(self):
        return self.borrowers
    
    def getLenders(self):
        return self.lenders
    
    def getDebt(self, neighbour):
        return abs(self.neighbours[neighbour])
    
    def getBrokeNeighbours(self):
        return self.brokes

    ''' SET FUNCTIONS '''
    def setBankruptcy(self, value):
        self.bankruptcy = value
        self.infection = value
    
    def setPosition(self, pos):
        self.position = pos
    
    def setLiquidity(self, liq):
        self.liquidity = liq
    
    def setCapital(self, chng):
        self.capital += chng

    def setBorrowers(self, borrowers):
        random.shuffle(borrowers)
        self.borrowers = borrowers      #Borrowers is unsorted 
    
    def setLenders(self, lenders):
        random.shuffle(lenders)
        self.lenders = lenders    #Lenders is unsorted
    
    def setNoDebt(self):
        for neighbour in self.neighbours:
            self.neighbours[neighbour] = 0 
    
    def setBrokeNeighbours(self, broke):
        random.shuffle(broke)
        self.brokes = broke
        
    ''' CHANGE FUNCTIONS for += type addition '''
    def changeLiquidity(self, chng):
        self.liquidity += chng

    def changeCapital(self, chng):
        self.capital += chng
    
    def changeDebt(self, neighbour, debt):
        self.neighbours[neighbour] += debt
        

    ''' Update functions don't take arguments. They are called and iterate through
        neighbors to set borrowers/lenders/broke neighbors, and set them internally
        without returning anything '''
    def updateBorrowersLenders(self):
        borrowers = []
        lenders = []
        for neighbour, value in self.neighbours.items():
            if value > 0 and (neighbour.getBankruptcy() is False):# and neighbour.getInfection() is False):
                borrowers.append(neighbour)
            elif value < 0 and (neighbour.getBankruptcy() is False):# and neighbour.getInfection() is False):
                lenders.append(neighbour)
        self.setBorrowers(borrowers)
        self.setLenders(lenders)
    
    def updateBrokeNeighbours(self):
        broke = []
        for neighbour in self.neighbours:
            if neighbour.getBankruptcy() is not True and neighbour.getCapital() < 0 and neighbour.getTotalDebt() < 0:
                broke.append(neighbour) 
        self.setBrokeNeighbours(broke)
        
    ''' MISCELLANEOUS FUNCTIONS '''
    
    ''' Transfer given amount of money from self to given neighbor, and update debt '''
    def transfer(self, neighbour, money):  #money is +ve when self to neighbour and -ve when it is neighbour to self
        self.changeLiquidity(-money)
        neighbour.changeLiquidity(money)
        self.changeDebt(neighbour, money)
        neighbour.changeDebt(self, -money)

    ''' This function is for network generation only.  '''
    def putNeighbours(self, neighbours, amount_withothers):
        self.neighbours = dict(zip(neighbours, amount_withothers))
        self.updateBorrowersLenders()

    ''' Set infection to false '''
    def cure(self):
        self.infection = False

    ''' Set infection to true. This function is called for all neighbors of a bankrupt bank,
        so '''
    def infect(self, bank = None):
        self.infection = True
        if not bank is None:  # this function is called for all neighbors of 
            self.loseMoney(bank)

    ''' ??? Where is this used? Why? '''
    def loseMoney(self, bank):
        self.changeCapital(-self.getDebt(bank))
        self.changeDebt(bank, -self.getDebt(bank))

    ''' Reset all attributes of a bank (used after bankruptcy avalanche is over) '''
    def reset(self):
        self.Bankruptcy = False
        self.infection = False
        self.capital = 0
        self.liquidity = 0
        self.setNoDebt()

    ''' Debugging function I think. Used to check if the capital still equals the liquidity + loans/debts. '''
    def isCapitalRight(self):
        if not self.getCapital() == self.getTotalDebt() + self.getLiquidity():
            raise Exception("Capital isn't right!")
            
    ''' This gets invoked when doing print(node). Print usefull stuff instead of node reference memory address '''
    def __str__(self):
        out = "Node %d has %d capital and %d liquidity. " %(self.getLabel(), self.getCapital(), self.getLiquidity())
        for n in self.neighbours:
            out += " %d debt to node %d. " % (self.neighbours[n], n.getLabel())
        return out

def createAdjacencyMatrix(network):
    """
    Returning the adjacency matrix of the network
    """
    matrix = nx.adjacency_matrix(network)
    return matrix

#if __name__ == "__main__" :
#    rows = 3
#    dimension = 2
#    banks = initializeBanks(rows**dimension)
#    network_map = createNetwork(rows, dimension)
#    network = linkBanks(network_map, banks)
#    
#    for bank in banks:
#        print(bank)