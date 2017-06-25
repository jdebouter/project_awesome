import generate_network as gn
import dynamics_network as dn
import analyze_network as an
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

def get_node_colours(network):
    to_return = []
    c = {}
    # for n in nx.get_node_attributes(G, 'capital').values():
    for n in G.nodes():
        liquidity = n.getLiquidity()
        capital = n.getCapital()
        c[n] = str(liquidity)
        # print (capital)
        if n.getTotalDebt() > 0:
            to_return.append(1)
        else:
            to_return.append(0)
        # if  capital < 0:
            # to_return.append(0)
        # elif capital > 0:
            # to_return.append(1)
        # else:
            # to_return.append(0)
    # print (to_return)
    return np.array(to_return), c
    # return np.array(list(nx.get_node_attributes(G,'capital').values()))

def get_edge_colours(network):
    to_return = []
    for n in G.nodes():
        neighbours = n.getNeighboursDict()
        for i in neighbours.keys():
            debt = neighbours[i]
            # print (debt)
            if debt != 0:
                G[n][i]['colour'] = 1
                # c[(n, i)] = abs(debt)
            else:
                G[n][i]['colour'] = -1
    # for n in G.nodes():
        # for i in G.neighbors(n):
            # to_return.append(G[n][i]['colour'])

    # print (to_return)
    for i, j  in nx.get_edge_attributes(G,'colour'):
        to_return.append(G[i][j]['colour'])

    return np.array(to_return)
    

random.seed(1)


def gen_graph(network, defaults):
    to_return = nx.DiGraph()

    nx.set_node_attributes(to_return, 'capital', 0) 
    nx.set_node_attributes(to_return, 'liquidity', 0) 
    nx.set_node_attributes(to_return, 'color', 0) 
    nx.set_node_attributes(to_return, 'bankrupt', 0) 

    nx.set_edge_attributes(to_return, 'debt', 0) 
    for n in network.nodes():
        to_return.add_node(n)
        to_return.node[n]['capital'] = n.getCapital()
        to_return.node[n]['liquidity'] = n.getLiquidity()
        if n.getLiquidity() < 0:
            to_return.node[n]['color'] = '0.75'
        elif n.getLiquidity() > 0:
            to_return.node[n]['color'] = '0.75'
        else:
            to_return.node[n]['color'] = '0.75'

        if n in defaults:
            print ("helloj w")
            to_return.node[n]['bankrupt'] = 1
            to_return.node[n]['color'] = 'r'
        else:
            to_return.node[n]['bankrupt'] = 0

        neighbours = n.getNeighboursDict()
        for i in neighbours.keys():
            debt = neighbours[i]
            if debt > 0:
                to_return.add_edge(*(n, i))
                to_return[n][i]['debt'] = debt
    return to_return
     

def graph_plot(network, step, node_size, font_size, label_edges = True):
    dn.run_simulation(network, step)
    
    G = gen_graph(network)
    # edges = G.edges()

    fig = plt.figure(figsize=(5,5))
    pos = nx.shell_layout(G)

    if label_edges:
        edge_labels = nx.get_edge_attributes(G,'debt')
        edge_labels = nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
    
    edges = nx.draw_networkx_edges(G, pos, alpha=.3, edge_color='k',  vmin=-1, vmax=1) 
    print (type(edges))

    node_color = [G.node[n]['color'] for n in G.nodes()]
    nodes = nx.draw_networkx_nodes(G, pos ,node_size=node_size, node_color=node_color, alpha=0.5, vmin=-1, vmax=1)
    nodes.set_cmap('RdYlGn')
    nodes.set_edgecolor('k')

    node_label = nx.get_node_attributes(G,'liquidity')
    node_labels = nx.draw_networkx_labels(G, pos, node_label, font_size=font_size)

    plt.axis('off')
    # plt.show()
    


def animate_simulation(network, node_size, fast = True):
    dn.step_simulation(network)

    fig = plt.figure(figsize=(5,5))
    fig.gca().set_xlim(left=-1.1, right=1.1)
    fig.gca().set_ylim(bottom=-1.1, top=1.1)
    plt.axis('off')

    G = gen_graph(network, [])

    pos = nx.shell_layout(G, scale=1)

    edges = nx.draw_networkx_edges(G, pos, alpha=.3, edge_color='k',  vmin=-1, vmax=1) 
    edges2 = nx.draw_networkx_edges(network, pos, alpha=.3, edge_color='k',  vmin=-1, vmax=1) 
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='w', vmin=-1, vmax=1)
    
    defaults = []
    def update(n):
        fig.clf()
 
        fig.gca().set_xlim(left=-1.1, right=1.1)
        fig.gca().set_ylim(bottom=-1.1, top=1.1)
        plt.axis("off")
        # if fast:
        defaults = dn.step_simulation(network)
        plt.title(str(n))
        print (np.ndarray.flatten(np.array(defaults)))
        # if defaults != []:
            # print ("hello")
        # else:
            # z = n % 4
            # if z == 0:
                # dn.perturb(network)
                # plt.title('Perturb')
            # elif z == 1: 
                # dn.repay_debts(network)
                # plt.title('Repay Debts')
            # elif z == 2:
                # dn.collect_loans(network)
                # plt.title('Collect Loans')
            # elif z == 3:
                # dn.invest_surplus_liquidity(network)
                # dn.check_and_propagate_avalanche(network, None)
                # plt.title('Invest Surplus Liquidity')
            # else:
                # assert(False)
 
        G = gen_graph(network, defaults)
        node_color = [G.node[n]['color'] for n in G.nodes()]

        edges = nx.draw_networkx_edges(G, pos,alpha=.3, edge_color='k',  vmin=-1, vmax=1) 
        edges2 = nx.draw_networkx_edges(network, pos, alpha=.1, edge_color='k',  vmin=-1, vmax=1) 
        nodes = nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, cmap='tab20c', vmin=-1, vmax=1)

        return nodes, edges, edges2

    ani = FuncAnimation(fig, update, interval=1000)
    plt.show()
    

G = gn.regular_network(L = 5, d = 2, Tl = -4, Ts = -6)
# G = gn.barabasi_albert_network(2, 2, Tl=-4, Ts=-2)
animate_simulation(G, 20)
# graph_plot(G, 20,120, 10)
# plt.savefig('1.png')
# graph_plot(G, 1,120, 10)
# plt.savefig('2.png')
# graph_plot(G, 1,120, 10)
# plt.savefig('3.png')
# graph_plot(G, 1,120, 10)
# plt.savefig('4.png')
# graph_plot(G, 1,120, 10)
# graph_plot(G, 20,120, 10)

# fig = plt.figure()
# d = []
# for i in range(10):
    # G = nx.barabasi_albert_graph(10, 2)
    # z = nx.draw(G, animated=True)
    # print (z)
    # d.append(z)

# ani = animation.ArtistAnimation(fig, d, interval=50, blit=True)
# plt.show()


