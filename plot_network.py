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

import aux
import plt_parameters

#%%

class Node:
    def __init__(self, node_name, link, dist_to_Qonnector, node_type, number_of_qubits=1):
        self._name = node_name
        self._link = link # Hub the node is connected to.
        self._dist = dist_to_Qonnector
        self._type = node_type # Qonnector, Qlient.
        self._keylist = []   # shared one-time pad
        self._number_of_qubits = number_of_qubits   # number of qubits for this node
        self._qubits = ns.qubits.create_qubits(number_of_qubits)


def state_to_graph_state(nodes, state=0):
    # takes a NetSquid state and returns the list of edges of the graph state. If no state is specify, the 
    
    edges = []
    if state==0:
        print('\nEmpty graph state.\n')
        return edges
    
    else:
        node_list = list(nodes.values())
        # TODO: finish the following block:
        # for i in range(len(node_list)):
            # for j in range(i, len(node_list)):
                # Hay que chequear si los qubits de i y j estan entrelazados.
                # TODO
                # print(i, j)
        for node in node_list[1:]:
            edges.append((node_list[0]._name, node._name))
            
            edges = list(set(edges))    # drops duplicates
        return edges


# S_edges = state_to_graph_state(nodes, state=ket_representation)
#%%

def draw_network(N, nodes, N_pos, parameters, S, plot_graph_state=True, step=0, ket=False, legend=False, show=True):
    # Takes a network N and a graph state S, both type nx.Graph(), and plots them.
    
    plt.figure()
    
    colours_dict = {'Qonnector': 'gray', 'Qlient': 'lightgray'}
    
    colours = []
    for node in nodes.values():
        colours.append(colours_dict[node._type])
    
    # cmap = plt.cm.coolwarm
    
    edge_labels = {}
    for node in nodes.values():
        edge = (node._name, node._links)
        edge_labels[edge] = r'$%g \, km$'%node._dist
    
    N_node_options = {"edgecolors": "tab:gray",
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
        
    nx.draw_networkx(N, pos=N_pos, node_color=colours, with_labels=True, labels=node_labels, **N_node_options)
    nx.draw_networkx_edges(N, N_pos, edge_color='black', width=1, alpha=1, label=r'network')
    
    edge_label_colour = 'blue'
    # edge_label_colour = plt.cm.coolwarm
    nx.draw_networkx_edge_labels(N, N_pos, edge_labels=edge_labels, font_color=edge_label_colour)
    
    
    if plot_graph_state:        
        nx.draw_networkx_edges(S, N_pos, edge_color='purple', width=5, alpha=0.5, label=r'$ | G \rangle $')
        nx.draw_networkx_edge_labels(N, N_pos, edge_labels=edge_labels, font_color=edge_label_colour)
    
    if ket:
        plt.suptitle(r'$| \psi \rangle = | %d \rangle$'%step) # TODO: tomar el string de la funcion que hasta ahora solo imprime.
    
    if legend:
        plt.legend()
    
    if show:
        plt.show()
    
    save_dir = 'plots' + os.sep + parameters['network']
    aux.check_dir(save_dir)
    
    plt.savefig(save_dir + os.sep + parameters['network'] + '_' + str(step) +'.png')

#%%



if __name__ == "__main__":
    
    parameters = aux.read_parameters('parameters')
    parameters['network'] = 'ParisianQuantumNetwork' #'QEurope'
    
    network = pd.read_csv('networks' + os.sep + parameters['network'] + '.csv', header=0)
    
    nodes = {}
    for n in range(len(network)):
        nodes[network['Name'].at[n]] = Node(network['Name'].at[n], network['Link'].at[n], network['Distance to Qonnector (km)'].at[n], network['Type'].at[n])
    
    PRINT_NODES_INFO = 0
    
    if PRINT_NODES_INFO:
        import pprint
        for node in nodes.values():
            pprint.pprint(vars(node), width=1)
    
    N = nx.Graph()
    edges = list(zip(network['Name'], network['Link']))
    N.add_edges_from(edges)
    
    N_pos = nx.spring_layout(N)
    
    ##############
    '''
    import netsquid as ns
    import local_complementation as lc
    
    n_qubits = 4
    Q = ns.qubits.create_qubits(n_qubits)
    lc.combine_Q(Q)
    lc.print_state()
    
    # Ket representation to Python list:
    ket_representation = list(Q[0].qstate.qrepr.ket)
    ket_representation = [int(item[0]) for item in ket_representation]
    '''
    
    ##############
    Graph_States = []
    
    for i in range(len(nodes)):
        S = nx.Graph()
        S_edges = state_to_graph_state(nodes, state=1) # TODO: state should later be the state, not a '1'.
        S_edges = S_edges[:i] # TODO: This line should be removed once state_to_graph_state() is actually working.
        S.add_edges_from(S_edges)
        Graph_States.append(S)
    
    for step in range(len(Graph_States)):
        draw_network(N, nodes, N_pos, parameters, S=Graph_States[step], plot_graph_state=1, step=step)
    
    # path = 'plots' + os.sep + parameters['network']
    # aux.check_dir(path)
    # plt.savefig(path + os.sep + parameters['network'] + '.png')
    
    ANIM = True
    
    if ANIM:
        import network_animation as na
        
        na.animation(parameters['network'])
