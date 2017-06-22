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
        
    def putNeighbours(self, neighbours, amount_withothers):
        self.neighbours = dict(zip(neighbours, amount_withothers))
        self.findBorrowersLenders()
        # The neighbours define the edges and the direction of them   
    
    ''' get methods for accessing attributes '''
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
    
    def setBrokeNeighbours(self, broke):
        random.shuffle(broke)
        self.brokes = broke
    
    ''' Change methods for += type addition '''
    
    def changeLiquidity(self, chng):
        self.liquidity += chng
#        self.setCapital(self.getLiquidity() + self.getTotalDebt())

    def changeCapital(self, chng):
        self.capital += chng
    
    def changeDebt(self, neighbour, debt):
        self.neighbours[neighbour] += debt

    ''' find functions go through neighbors and set borrowers/lenders/broke banks
        to corresponding attributes '''
        
    def findBorrowersLenders(self):
        borrowers = []
        lenders = []
        for neighbour, value in self.neighbours.items():
            if value > 0:
                borrowers.append(neighbour)
            elif value < 0:
                lenders.append(neighbour)
        self.setBorrowers(borrowers)
        self.setLenders(lenders)
    
    def findBrokeNeighbours(self):
        broke = []
        for neighbour in self.neighbours:
            if neighbour.getLiquidity() < 0:
                broke.append(neighbour)
        self.setBrokeNeighbours(broke)
    
    ''' Transfer given amount of money from self to given neighbor'''
    def transfer(self, neighbour, money):  #money is +ve when self to neighbour and -ve when it is neighbour to self
        self.changeLiquidity(-money)
        neighbour.changeLiquidity(money)
        self.changeDebt(neighbour, money)
        neighbour.changeDebt(self, -money)
        
    ''' For printing a Bank object '''
    def __str__(self):
        out = "Node %d has %d capital and %d liquidity. " %(self.getLabel(), self.getCapital(), self.getLiquidity())
        for n in self.neighbours:
            out += " %d debt to node %d. " % (self.neighbours[n], n.getLabel())
        return out

# Define the banking grid with a unbalanced grid
def initializeBanks(tot_banks):
    banks = []
#    capital = range(-2, 3)
    for i in range(tot_banks):
#        bank = Bank(i, random.choice(capital))
        bank = Bank(i, 0)
        banks.append(bank)
#    maximum_neighbours = 4
#    assignNeighbours(banks, maximum_neighbours)
    return banks

# Neighbours are assignmed  
def _assignNeighbours(network):
    for node in network.nodes():
        node.putNeighbours(network.neighbors(node),[0]*len(network.neighbors(node)))
        

# Interbanking is initiated
def startInterbankTrading(banks):
    while True:
        trade(banks)

# Trade Implementation
def trade(banks):
    pass


def linkBanks(G, banks):
    """
    Objects of the Bank class are assigned as Nodes
    Also, a adjacency matrix for this network is printed
    """
    
    # Relabelling the nodes to that of the objects of the class Bank
    mapping = dict(zip(G.nodes(), banks))
    grid = nx.relabel_nodes(G, mapping)
    # Assigning a position to banks according to the ordering in the network
    i = 0
    for nodes in grid.nodes():
        nodes.setPosition(i)
        i += 1
    # Creating the adjacency matrix
#    print(createAdjacencyMatrix(grid))
    # Drawing the graph
    bank_positions = [nodes.getLabel() for nodes in grid.nodes()]
    bank_labels = dict(zip(grid.nodes(), bank_positions))
#    nx.draw(grid, labels = bank_labels, with_labels = True)
#    plt.show()
    _assignNeighbours(grid)
    
    return grid

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