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
    print(avalanche_sizes)
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
    ax.legend()
    # ax.legend(loc='lower left')
    plt.show()

def plot_network(network):
    pos=nx.circular_layout(network)
    nx.draw_networkx_edges(network, pos=pos, alpha=.1, edge_color='k')
    nx.draw_networkx_nodes(network, pos=pos, node_color = 'b', node_size = 1)
    plt.show()

def calc_average_degree(network):
    return np.mean(list(network.degree().values()))

from scipy import stats
# import statsmodels.api as sm
def fit_line(x, y):
    p, V = np.polyfit(x, y, 1, cov=True)
    slope = p[0]
    intercept = p[1]
    slope_confidence_interval = np.sqrt(V[0][0])
    intercept_confidence_interval = np.sqrt(V[1][1])
    return slope, intercept, slope_confidence_interval, intercept_confidence_interval

def histogram_avalanches(avalanche_sizes, num_bins):
    hist, bin_edges = np.histogram(avalanche_sizes, bins=num_bins)
    return hist, bin_edges

''' Plot a histogram of the avalanche sizes '''
def plot_avalanches(avalanche_sizes, label, color, token='*', num_bins = 100, plot = False):
    # Setup plot.
    font = {'family' : 'normal', 'weight' : 'bold', 'size'   : 16}
    mpl.rc('font', **font)
    plt.yscale('log')
    plt.xscale('log')

    # Plot histogram
    hist, bin_edges = histogram_avalanches(avalanche_sizes, num_bins)
    x = np.linspace(1, max(avalanche_sizes), num_bins)
    if plot:
        plt.plot(x, hist, token, label=label, color=color)

    y = hist[hist>0]
    x = x[hist>0]

    slope, intercept, slope_confidence_interval, intercept_confidence_interval = fit_line(np.log(x), np.log(y))
    y_fit = np.power(x, slope) * np.exp(intercept)
    if plot:
        plt.plot(x, y_fit, alpha=.5, color=color)
    # plt.show()

    return slope, intercept, slope_confidence_interval, intercept_confidence_interval


def confidencePlot(parametervalues, mean, std):

#    font = {'family' : 'normal', 'weight' : 'bold', 'size' : 16}
#    mpl.rc('font', **font)
#
    if len(parametervalues) > 2:
        plt.errorbar(parametervalues, mean, yerr=std, color='b', fmt='--o', capsize=4)
    else:
        plt.errorbar(parametervalues[0], mean[0], yerr=std[0], fmt='o', capsize=4, color='b')
        plt.errorbar(parametervalues[1], mean[1], yerr=std[1], fmt='o', capsize=4, color='g')
        plt.xticks(parametervalues, ['False', 'True'])
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    plt.xlim((xmin-0.1, xmax+0.1))
    plt.ylim((ymin-1, ymax+1))
    # plt.show()
