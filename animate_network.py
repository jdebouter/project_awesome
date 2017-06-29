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
    



def gen_graph(network, defaults):
    to_return = nx.DiGraph()

    nx.set_node_attributes(to_return, 'capital', 0) 
    nx.set_node_attributes(to_return, 'liquidity', 0) 
    nx.set_node_attributes(to_return, 'color', 0) 
    nx.set_node_attributes(to_return, 'bankrupt', 0) 

    nx.set_edge_attributes(to_return, 'debt', 0) 
    nx.set_edge_attributes(to_return, 'color', 'k') 
    for n in network.nodes():
        to_return.add_node(n)
        to_return.node[n]['capital'] = n.getCapital()
        to_return.node[n]['liquidity'] = n.getLiquidity()
        if n.getLiquidity() < 0:
            # to_return.node[n]['color'] = 'forestgreen'
            to_return.node[n]['color'] = -1
        elif n.getLiquidity() > 0:
            # to_return.node[n]['color'] = 'forestgreen'
            to_return.node[n]['color'] = 1
        else:
            # to_return.node[n]['color'] = 'forestgreen'
            to_return.node[n]['color'] = 0

        if n in defaults:
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
                to_return[n][i]['color'] = 'k'
    return to_return
     

def graph_plot(network, step, node_size, font_size, label_edges = True):
    dn.run_simulation(network, step)
    
    G = gen_graph(network, [])
    # edges = G.edges()

    fig = plt.figure(figsize=(5,5))
    pos = nx.shell_layout(G)

    if label_edges:
        edge_labels = nx.get_edge_attributes(G,'debt')
        
        edge_labels = nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
    
    edges = nx.draw_networkx_edges(G, pos, alpha=1, edge_color='k',  vmin=-1, vmax=1, arrows=False) 
    nx.draw_networkx_edges(network, pos, alpha=.1, edge_color='k',  vmin=-1, vmax=1) 
    
    print (type(edges))

    node_color = [G.node[n]['color'] for n in G.nodes()]
    nodes = nx.draw_networkx_nodes(G, pos ,node_size=node_size, node_color=node_color, alpha=0.5, vmin=-1, vmax=1)
    nodes.set_cmap('RdYlGn')
    nodes.set_edgecolor('k')

    node_label = nx.get_node_attributes(G,'liquidity')
    node_labels = nx.draw_networkx_labels(G, pos, node_label, font_size=font_size)

    plt.axis('off')
    plt.show()
    
def basic_graph_plot(G, node_size):

    fig = plt.figure(figsize=(5,5))
    pos = nx.shell_layout(G)

   
    edges = nx.draw_networkx_edges(G, pos, alpha=.5, edge_color='k',  vmin=-1, vmax=1) 
    # nx.draw_networkx_edges(G, pos, alpha=.1, edge_color='k',  vmin=-1, vmax=1) 
    

    # node_color = [G.node[n]['color'] for n in G.nodes()]
    nodes = nx.draw_networkx_nodes(G, pos ,node_size=node_size, node_color='k', alpha=1, vmin=-1, vmax=1)
    # nodes.set_cmap('RdYlGn')
    # nodes.set_edgecolor('k')

    # node_label = nx.get_node_attributes(G,'liquidity')
    # node_labels = nx.draw_networkx_labels(G, pos, node_label, font_size=font_size)

    plt.axis('off')
    plt.show()
    



def animate_simulation(network, node_size):
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

        defaults = dn.step_simulation(network)
        plt.title(str(n))
        G = gen_graph(network, defaults)
        node_color = [G.node[n]['color'] for n in G.nodes()]

        edges = nx.draw_networkx_edges(G, pos,alpha=1, edge_color='k', arrows=False) 
        edges2 = nx.draw_networkx_edges(network, pos, alpha=.1, edge_color='k') 
        nodes = nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color)

        return nodes, edges, edges2

    ani = FuncAnimation(fig, update, interval=600, frames=100)
    ani.save('2osc2.mp4', writer="ffmpeg")
    plt.show()
   
def default_graph(defaults, network):
    G = nx.DiGraph()
    
    for n in defaults:
        G.add_node(n)

    for n in G.nodes():
        for i in network.neighbors(n):
            if G.has_node(i):
                G.add_edge(*(n, i))
    starts = []
    for n in G.nodes():
        if G.in_degree(n) == 0:
            starts.append(n)

    to_return = []
    for n in starts:
        to_return.append(n)
        z = []
        z.append(n)
        while (len(z) > 0):
            h = z.pop(0)
            for i in G.neighbors(h):
                z.append(i)
                to_return.append(i)
        break;
    # to_return = to_return[:-1]
    print (len(to_return))
    # nx.draw(G)
    # plt.show()
    return to_return

def animate_defaults2(node_size):

    G = nx.Graph()
    nx.set_node_attributes(G, 'color', 0) 
    nx.set_edge_attributes(G, 'color', 0) 
    for i in range(10):
        G.add_node(i)

    for i in [0,3,1,4,5]:
        for j in [8,2]:
            G.add_edge(i,j)
            G[i][j]['color'] = 'k'
    for i in [6,7,9]:
        for j in [8,2]:
            G.add_edge(i,j)
            G[i][j]['color'] = '0.75'


    fig = plt.figure(figsize=(5,5))
    fig.gca().set_xlim(left=-1.1, right=1.1)
    fig.gca().set_ylim(bottom=-1.1, top=1.1)
    plt.axis('off')

    for n in G.nodes():
        G.node[n]['color'] = 'g'

    pos = nx.shell_layout(G, scale=1)

    edges = nx.draw_networkx_edges(G, pos, alpha=.3, edge_color='k',  vmin=-1, vmax=1) 
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='k')

    def update(n):
        if n ==1 :
            G.node[0]['color'] = 'r'
        if n == 2:
            G[0][8]['color'] = 'r'
            G[0][2]['color'] = 'r'
        if n == 3:
            G.node[8]['color'] = 'r'
            G.node[2]['color'] = 'r'
        if n == 4:
            G[8][0]['color'] = 'r'
            G[8][3]['color'] = 'r'
            G[8][1]['color'] = 'r'
            G[8][4]['color'] = 'r'
            G[8][5]['color'] = 'r'
        if n == 5:
            G.node[5]['color'] = 'r'
        if n == 6:
            # G.node[5]['color'] = 'r'
            G[5][2]['color'] = 'r'
        if n == 7:
            G.node[3]['color'] = 'r'
        if n == 8:
            G[3][2]['color'] = 'r'





        fig.clf()
        fig.gca().set_xlim(left=-1.1, right=1.1)
        fig.gca().set_ylim(bottom=-1.1, top=1.1)
        plt.axis("off")

        node_color = [G.node[n]['color'] for n in G.nodes()]
        edge_color = [G[u][v]['color'] for u, v in G.edges()]

        edges = nx.draw_networkx_edges(G, pos,alpha=.7, width=2,edge_color=edge_color, arrows=True) 
        nodes = nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color)

        return nodes, edges

    ani = FuncAnimation(fig, update, interval=1000)
    ani.save('2osc2.mp4', writer="ffmpeg")
    plt.show()
 
def animate_defaults(network, avalanche_size, node_size):
    dn.step_simulation(network)
    defaults = []
    while (len(defaults) < avalanche_size):
        G = gen_graph(network, [])
        defaults = dn.step_simulation(network)
        # print (defaults.flatten())
        # defaults = set(defaults.tyyp.flatten())
        try:
            defaults = set(defaults.flatten().tolist())
            # print ("hello")
        except:
            defaults = []

    d = default_graph(defaults, G)

    fig = plt.figure(figsize=(5,5))
    fig.gca().set_xlim(left=-1.1, right=1.1)
    fig.gca().set_ylim(bottom=-1.1, top=1.1)
    plt.axis('off')

    for n in G.nodes():
        G.node[n]['color'] = 'g'
    pos = nx.shell_layout(G, scale=1)

    edges = nx.draw_networkx_edges(G, pos, alpha=.3, edge_color='k',  vmin=-1, vmax=1) 
    edges2 = nx.draw_networkx_edges(network, pos, alpha=.3, edge_color='k',  vmin=-1, vmax=1) 
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='w', vmin=-1, vmax=1)
    # for n in defaults:
        # print (G.nodes[n].in_degree())
    def update(n):
        if not len(d) == 0:
            x = d.pop(0)
            G.node[x]['color'] = 'r'
            for i in G.nodes():
            # for i in G.neighbors(x):
                # network[i][x]['color'] = 'r'
                try:
                    G[i][x]['color'] = 'r'
                    G.node[i]['color'] = 'r'
                except:
                    pass


        # z = n % 2
        # if z == 0:
            # x = d[0]
            # G.node[x]['color'] = 'r'
        # elif len(d) == 0:
            # pass
        # else:
            # x = d.pop(0)
            # for i in G.neighbors(x):
                # network[i][x]['color'] = 'r'
                # # G[x][i]['color'] = 'r'
                # G.node[i]['color'] = 'r'


        fig.clf()
        fig.gca().set_xlim(left=-1.1, right=1.1)
        fig.gca().set_ylim(bottom=-1.1, top=1.1)
        plt.axis("off")

        # plt.title(str(n))
        node_color = [G.node[n]['color'] for n in G.nodes()]
        edge_color = [G[u][v]['color'] for u, v in G.edges()]

        edges = nx.draw_networkx_edges(G, pos,alpha=1, edge_color=edge_color, arrows=True) 
        edges2 = nx.draw_networkx_edges(network, pos, alpha=.1, edge_color='k') 
        nodes = nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color)

        return nodes, edges, edges2

    ani = FuncAnimation(fig, update, interval=1000, frames=len(defaults))
    ani.save('2osc2.mp4', writer="ffmpeg")
    plt.show()
 
# import pickle
# random.seed()
# import matplotlib
# matplotlib.use("Agg")
# Writer = animation.writers['ffmpeg']
# network = gn.mean_field_network(9, 1, 1, c = 1, m = 0.52)
# network = pickle.load(open("MEAN_FIELD_SAVED/mean_field_N100_tl-4_ts-6.pickle", "rb" ))
random.seed(1)
# network = gn.regular_network(L = 8, d = 2, Tl = -4, Ts = -6)
# network.graph['Tl'] = -2
# network.graph['Ts'] = -20

# network = gn.barabasi_albert_network(50, 3, Tl=-4, Ts=-2)
# network.graph['Tl'] = -1
# network.graph['Ts'] = -20
# basic_graph_plot(network, 40)
# animate_simulation(network, 15)
# graph_plot(network, 10, 40, 5)
# animate_defaults(network, 10, 15)
animate_defaults2(50)

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
 

