# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 17:45:48 2017

@author: krish
"""

"""
Just implementing the whole thing without networks.
We will colloborate it to the main one on Tuesday 
"""

import random 
import networkx as nx
import matplotlib.pyplot as plt

global SOLVENCY_THRESHOLD, LIQUIDITY_THRESHOLD 
SOLVENCY_THRESHOLD = -5
LIQUIDITY_THRESHOLD = -3

# Definition of a Banking Node 

class Bank(object):
    def __init__(self, node, amount_inhand, amount_withothers = []):
        self.position = node
        self.capital = sum(amount_withothers) + amount_inhand
        self.liquidity = amount_inhand
            
    def putNeighbours(self, neighbours, amount_withothers):
        self.neighbours = dict(zip(neighbours, amount_withothers))
        # The neighbours define the edges and the direction of them   
    
    def getPosition(self):
        return self.position
    
    def getLiquidity(self):
        return self.liquidity
        
    def getCapital(self):
        return self.capital
    
    def getNeighbours(self):
        return self.neighbours.keys()
    
    def getDebt(self, neighbour):
        return self.neighbours[neighbours]
    
    def setPosition(self, pos):
        self.position = pos
    
    def changeCapital(self, chng):
        self.capital += chng
        
    def __str__(self):
        return "The Bank %d had %d Capital" %(self.getPosition(), self.getCapital())

# Define the banking grid with a unbalanced grid
def initializeBanks(tot_banks):
    banks = []
    capital = range(-2, 3)
    for i in range(tot_banks):
        bank = Bank(i, random.choice(capital))
        banks.append(bank)
#    maximum_neighbours = 4
#    assignNeighbours(banks, maximum_neighbours)
    return banks

# Neighbours are assignmed  
def assignNeighbours(banks, maximum_neighbours):
    pass

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
    print createAdjacencyMatrix(grid)
    # Drawing the graph
    bank_positions = [nodes.getPosition() for nodes in grid.nodes()]
    bank_labels = dict(zip(grid.nodes(), bank_positions))
    nx.draw(grid, labels = bank_labels, with_labels = True)
    plt.show()


def createAdjacencyMatrix(network):
    """
    Returning the adjacency matrix of the network
    """
    matrix = nx.adjacency_matrix(network)
    return matrix

if __name__ == "__main__" :
    rows = 3
    dimension = 2
    banks = initializeBanks(rows**dimension)
#    createLatticeNetwork(banks, rows, dimension)
    
    for bank in banks:
        print bank