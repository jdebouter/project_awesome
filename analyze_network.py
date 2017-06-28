""" ===========================================================================

This script is where we define the functions for network analysis.

=========================================================================== """


import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

''' Print the capital, liquidity and loans/debts for every node '''
def print_network(network):
    for node in network.nodes():
        print(node)
    print('\n')

''' Print the capital, liquidity and loans/debts for given nodes'''
def print_node_list(node_list):
    for node in node_list:
        print(node)
        print('\n')
    print('\n')

''' Plot a histogram of the avalanche sizes '''
def histogram_avalanches(avalanche_sizes, avalanche_sizes2 = None, num_bins = 50, y_scale = 'log', x_scale = 'log', labels = []):
    font = {'family' : 'normal', 'weight' : 'bold', 'size'   : 16}
    mpl.rc('font', **font)
    plt.figure(figsize=(10,6))
    results_histogram = np.histogram(avalanche_sizes, bins=num_bins)
    plt.plot(np.linspace(0, max(avalanche_sizes), num_bins), results_histogram[0], '*', color = 'blue', label = labels[0])
    print("1st sim: %i banks defaulted in total" % sum(avalanche_sizes))
    if not avalanche_sizes2 is None:
        results_histogram = np.histogram(avalanche_sizes2, bins=num_bins)
        plt.plot(np.linspace(0, max(avalanche_sizes2), num_bins), results_histogram[0], '^', color = 'green', label = labels[1])
        print("2nd sim: %i banks defaulted in total" % sum(avalanche_sizes2))
    plt.yscale(y_scale)
    plt.xscale(x_scale)
    plt.xlabel("Avalanche Size")
    plt.ylabel("Frequency")
    ax = plt.gca()
    ax.legend(loc='lower left')
    plt.show()

def plot_network(network):
    pos=nx.circular_layout(network)
    nx.draw_networkx_edges(network, pos=pos, alpha=.1, edge_color='k')
    nx.draw_networkx_nodes(network, pos=pos, node_color = 'b', node_size = 1)
    plt.show()

def calc_average_degree(network):
    return np.mean(list(network.degree().values()))

