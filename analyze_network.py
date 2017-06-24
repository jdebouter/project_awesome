""" ===========================================================================

This script is where we define the functions for network analysis.

=========================================================================== """


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

''' Print the capital, liquidity and loans/debts for every node '''
def print_network(network):
    for node in network.nodes():
        print(node)
    print('\n')

''' Plot a histogram of the avalanche sizes '''
def histogram_avalanches(avalanche_sizes, num_bins = 50, y_scale = 'log', x_scale = 'log'):
    results_histogram = np.histogram(avalanche_sizes, bins=num_bins)
    plt.plot(np.linspace(0, max(avalanche_sizes), num_bins), results_histogram[0], '*')
    plt.yscale(y_scale)
    plt.xscale(x_scale)
    plt.xlabel("Avalanche Size")
    plt.ylabel("Frequency")
    plt.show()

def plot_network(network):
    pos=nx.circular_layout(network)
    nx.draw_networkx_edges(network, pos=pos, alpha=.1, edge_color='k')
    nx.draw_networkx_nodes(network, pos=pos, node_color = 'b', node_size = 1)
    plt.show()

def calc_average_degree(network):
    return np.mean(list(network.degree().values()))

