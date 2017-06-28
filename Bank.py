# -*- coding: utf-8 -*-
"""
Krish's script where he defines the bank object. This script
should be renamed
"""

import random 
import networkx as nx
import dynamics_network as dn

BALANCE = dn.BALANCE

# Definition of a Banking Node 

class Bank(object):
    hub = False
    delta = 0
    injection = 0
    
    def __init__(self, node, amount_inhand, amount_withothers = []):
        self.label = node
        self.capital = sum(amount_withothers) + amount_inhand
        self.liquidity = amount_inhand
        self.bankruptcy = False
        self.infection = False
        self.neighbours = {}
        self.rich_neighbours = []
        self.money_lost = 0

    ''' GET FUNCTIONS '''
    def getTest(self):
        return self.test
    
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
     
    def getNeighboursDict(self):
        return self.neighbours
    
    def getTotalDebt(self):
        return sum(self.neighbours.values())
    
    def getBankruptcy(self):
        return self.bankruptcy
    
    def getBorrowers(self):
        self.updateBorrowersLenders()
        return self.borrowers
    
    def getLenders(self):
        self.updateBorrowersLenders()
        return self.lenders
    
    def getDebt(self, neighbour):
        return abs(self.neighbours[neighbour])
    
    def getRichNeighbours(self):
        self.updateRichNeighbours()
        return self.rich_neighbours

    def getMoneyLost(self):
        return self.money_lost
    
    ''' SET FUNCTIONS '''
    def setBankruptcy(self, value):
        self.bankruptcy = value
        self.infection = value
    
    def setPosition(self, pos):
        self.position = pos
    
    def setLiquidity(self, liq):
        self.liquidity = liq
    
    def setCapital(self, chng):
        self.capital = chng

    def setBorrowers(self, borrowers):
        random.shuffle(borrowers)
        self.borrowers = borrowers      #Borrowers is unsorted 
    
    def setLenders(self, lenders):
        random.shuffle(lenders)
        self.lenders = lenders    #Lenders is unsorted
    
    def setNoDebt(self):
        for neighbour in self.neighbours:
            self.neighbours[neighbour] = 0
            neighbour.neighbours[self] = 0
    
    def setRichNeighbours(self, rich_neighbours):
        random.shuffle(rich_neighbours)
        self.rich_neighbours = rich_neighbours
        
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
        for neighbour in self.getNeighbours():
            value = self.neighbours[neighbour]
            if value > 0 and (neighbour.getBankruptcy() is False):# and neighbour.getInfection() is False):
                borrowers.append(neighbour)
                
            elif value < 0 and (neighbour.getBankruptcy() is False):# and neighbour.getInfection() is False):
                lenders.append(neighbour)
        self.setBorrowers(borrowers)
        self.setLenders(lenders)
    
    def updateRichNeighbours(self):
        rich_neighbours = []
        for neighbour in self.neighbours:
            if neighbour.getCapital() > BALANCE and neighbour.getLiquidity() > BALANCE:
                rich_neighbours.append(neighbour) 
        self.setRichNeighbours(rich_neighbours)
        
    ''' MISCELLANEOUS FUNCTIONS '''
    
    ''' Transfer given amount of money from self to given neighbor, and update debt '''
    def transfer(self, neighbour, money):  #money is +ve when self to neighbour and -ve when it is neighbour to self
        self.changeLiquidity(-money)
        neighbour.changeLiquidity(money)
        self.changeDebt(neighbour, money)
        neighbour.changeDebt(self, -money)
        
    def lenderBorrowerSame(self):
        for neighbour in self.getNeighbours():
            if not self.getDebt(neighbour) == neighbour.getDebt(self):
                raise Exception("This doesn't make senseB!")

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
        
        if not bank is None:  # When this function is called for neighbours of an infected (not bankrupt) bank, the bank argument isn't set, so the neighbour doesn't lose money. When this function is called for neighbours of bankrupt banks, bank is set to something, and the neighbours lose capital appropriately
            self.loseMoney(bank)

    ''' DESCRIPTION '''
    def loseMoney(self, bank):
        self.money_lost += self.getDebt(bank)
        self.changeCapital(-self.getDebt(bank))
        bank.changeDebt(self, self.getDebt(bank))
        self.changeDebt(bank, -self.getDebt(bank))
         
                
    ''' Reset all attributes of a bank (used after bankruptcy avalanche is over) '''
    def reset(self):
        self.bankruptcy = False
        self.infection = False
        self.capital = BALANCE
        self.liquidity = BALANCE
        self.setNoDebt()
        self.injection = False
        self.money_lost = 0

    ''' Debugging function I think. Used to check if the capital still equals the liquidity + loans/debts. '''
    def isCapitalRight(self):
        if not self.getCapital() == self.getTotalDebt() + self.getLiquidity():
            print(self)
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
