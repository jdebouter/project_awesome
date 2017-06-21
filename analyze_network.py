# Testing.
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def print_network(network):
    print('\n\n\n')
    for node in network.nodes_iter(data=True):
        print(node)
    print()
    for edge in network.edges_iter(data=True):
        print(edge)

def histogram_avalanches(avalanche_sizes, num_bins = 10):
    results_histogram = np.histogram(avalanche_sizes, bins=num_bins)
    plt.plot(range(num_bins), results_histogram[0])
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
