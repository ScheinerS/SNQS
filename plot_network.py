#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:58:28 2023

@author: santiago
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import os
import aux
import netsquid as ns

import plt_parameters

#%%

class Node:
    def __init__(self, node_name, link, dist_to_Qonnector, node_type):
        self._name = node_name
        self._link = link # Hub the node is connected to.
        self._dist = dist_to_Qonnector
        self._type = node_type # Qonnector, Qlient.
        self._keylist = []   # shared one-time pad
        self._qubit = ns.qubits.create_qubits(1)


def state_to_graph_state(nodes, state=0):
    # takes a NetSquid state and returns the list of edges of the graph state. If no state is specify, the 
    
    edges = []
    if len(state)==0:
        print('\nEmpty graph state.\n')
        return edges
    
    else:
        node_list = list(nodes.values())
        for i in range(len(node_list)):
            for j in range(i, len(node_list)):
                # Hay que chequear si los qubits de i y j estan entrelazados.
                # TODO
                print(i, j)
        for node in nodes.values():
            edges.append((node._name, 'Jussieu'))
            
            edges = list(set(edges))    # drops duplicates
        return edges


# S_edges = state_to_graph_state(nodes, state=ket_representation)
#%%

def draw_network(N, nodes, parameters, Graph_State=nx.Graph(), plot_graph_state=0):
    # Takes a network N and a graph state S, both type nx.Graph(), and plots them.
    colours_dict = {'Qonnector': 'gray', 'Qlient': 'lightgray'}
    
    colours = []
    for node in nodes.values():
        colours.append(colours_dict[node._type])
    
    # cmap = plt.cm.coolwarm
    
    edge_labels = {}
    for node in nodes.values():
        edge = (node._name, node._link)
        edge_labels[edge] = r'$%g \, km$'%node._dist
    
    pos = nx.spring_layout(N)
    
    options = {"edgecolors": "tab:gray",
               "node_size": 800,
               "alpha": 0.9,
               'font_color': 'black',
               'verticalalignment': 'center',
               'horizontalalignment': 'center',
               'width': 1,
               'linewidths': 1}
    
    node_labels = {}
    for node in N.nodes():
        node_labels[node] = r'%s'%node
        
    nx.draw_networkx(N, pos=pos, node_color=colours, with_labels=True, labels=node_labels, **options)

    nx.draw_networkx_edge_labels(N, pos, edge_labels=edge_labels, font_color='red')
    
    
    if plot_graph_state:
        GS = nx.Graph()
        for node in nodes.values():
            GS.add_edge(node._name, 'Jussieu')
        
        nx.draw_networkx_edges(GS, pos, edge_color='lightblue')
    
    plt.show()
    save_dir = 'plots'
    aux.check_dir(save_dir)
    plt.savefig(save_dir + os.sep + parameters['network'] +'.png')
#%%

if __name__ == "__main__":
    
    parameters = aux.read_parameters('parameters')
    parameters['network'] = 'QEurope'
    
    network = pd.read_csv('networks' + os.sep + parameters['network'] + '.csv', header=0)
    
    nodes = {}
    for n in range(len(network)):
        nodes[network['Name'].at[n]] = Node(network['Name'].at[n], network['Link'].at[n], network['Distance to Qonnector (km)'].at[n], network['Type'].at[n])

    N = nx.Graph()
    edges = list(zip(network['Name'], network['Link']))
    N.add_edges_from(edges)
    
    ##############
    import netsquid as ns
    import local_complementation as lc
    '''
    Q = ns.qubits.create_qubits(n_qubits)
    lc.combine_Q(Q)
    lc.print_state()
    
    # Ket representation to Python list:
    ket_representation = list(Q[0].qstate.qrepr.ket)
    ket_representation = [int(item[0]) for item in ket_representation]
    '''
    
    ##############
    S = nx.Graph()
    S_edges = state_to_graph_state(nodes, state=0)
    S.add_edges_from(S_edges)

    draw_network(N, nodes, parameters, Graph_State=S, plot_graph_state=1)
    
