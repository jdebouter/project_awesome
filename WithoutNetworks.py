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
        self.Bankruptcy = False
        self.infection = False
        
    def putNeighbours(self, neighbours, amount_withothers):
        self.neighbours = dict(zip(neighbours, amount_withothers))
        self.areYouInDebt()
        # The neighbours define the edges and the direction of them   
    
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
    
    def getLenders(self):
        return self.lenders
    
    def getDebt(self, neighbour):
        return abs(self.neighbours[neighbour])
    
    def getBrokeNeighbours(self):
        return self.brokes

    ''' Set methods for setting attributes '''
    def setBankruptcy(self, value):
        self.bankruptcy = value
    
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
        
    def changeLiquidity(self, chng): 
        self.liquidity += chng 
#        self.setCapital(self.getLiquidity() + self.getTotalDebt()) 
        
    def infect(self):
        self.infection = True
#    
    def reset(self):
        self.Bankruptcy = False
        self.capital = 0
        self.liquidity = 0
        self.setNoDebt()
    
    def cure(self):
        self.infection = False
    
    def findBorrowersLenders(self):
        borrowers = []
        lenders = []
        for neighbour, value in self.neighbours.items():
            if value > 0 and (neighbour.getBankruptcy() is False):# and neighbour.getInfection() is False):
                borrowers.append(neighbour)
            elif value < 0 and (neighbour.getBankruptcy() is False):# and neighbour.getInfection() is False):
                lenders.append(neighbour)
        self.setBorrowers(borrowers)
        self.setLenders(lenders)
    
    def findBrokeNeighbours(self):
        broke = []
        for neighbour in self.neighbours:
            if neighbour.getLiquidity() < 0 and neighbour.getBankruptcy is not True:
                broke.append(neighbour)
        self.setBrokeNeighbours(broke)

    ''' WRITE DESCRIPTION'''
    def putNeighbours(self, neighbours, amount_withothers):
        self.neighbours = dict(zip(neighbours, amount_withothers))
        self.findBorrowersLenders()

    ''' Transfer given amount of money from self to given neighbor'''
    def transfer(self, neighbour, money):  #money is +ve when self to neighbour and -ve when it is neighbour to self
        self.changeLiquidity(-money)
        neighbour.changeLiquidity(money)
        self.changeDebt(neighbour, money)
        neighbour.changeDebt(self, -money)
    
    def __str__(self):
        out = "Node %d has %d capital and %d liquidity. " %(self.getLabel(), self.getCapital(), self.getLiquidity())
        for n in self.neighbours:
            out += " %d debt to node %d. " % (self.neighbours[n], n.getLabel())
        return out




        

# Interbanking is initiated
def startInterbankTrading(banks):
    while True:
        trade(banks)

# Trade Implementation
def trade(banks):
    pass



def createNetwork(rows, dimension):
    return nx.grid_graph([rows for i in range(dimension)], periodic=False)
    
    
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