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

global SOLVENCY_THRESHOLD, LIQUIDITY_THRESHOLD 
SOLVENCY_THRESHOLD = -5
LIQUIDITY_THRESHOLD = -3

# Definition of a Banking Node 

class Bank(object):
    def __init__(self, node, amount_inhand, amount_withothers = []):
        self.position = node
        self.capital = sum(amount_withothers) + amount_inhand
            
    def putNeighbours(self, neighbours, amount_withothers):
        self.neighbours = dict(zip(neighbours, amount_withothers))
        # The neighbours define the edges and the direction of them   
    
    def getPosition(self):
        return self.position
    
    def getCapital(self):
        return self.capital
    
    def getNeighbours(self):
        return self.neighbours.keys()
    
    def getDebt(self, neighbour):
        return self.neighbours[neighbours]
   
    def __str__(self):
        return "The Bank %d had %d Capital" %(self.getPosition(), self.getCapital())

# Define the banking grid with a unbalanced grid
def initializeBanks(tot_banks):
    banks = []
    capital = range(-2, 3)
    for i in range(tot_banks):
        bank = Bank(i, random.choice(capital))
        banks.append(bank)
    maximum_neighbours = 4
    assignNeighbours(banks, maximum_neighbours)
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


if __name__ == "__main__" :
    total_banks = 10
    banks = initializeBanks(10)
    for bank in banks:
        print bank