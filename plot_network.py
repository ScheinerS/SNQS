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

#%%

def draw_network(G, nodes, parameters, graph_state=0):
    
    plt.close('all')
    plt.rcParams['text.usetex'] = True
    
    colours_dict = {'Qonnector': 'gray', 'Qlient': 'lightgray'}
    
    colours = []
    for node in nodes.values():
        colours.append(colours_dict[node._type])
    
    cmap = plt.cm.coolwarm
    
    edge_labels = {}
    for node in nodes.values():
        edge = (node._name, node._link)
        edge_labels[edge] = '%g km'%node._dist
    
    pos = nx.spring_layout(G)
    
    # nx.draw_networkx(G, with_labels=True)
    nx.draw_networkx(G, pos=pos, cmap=cmap, node_color=colours, with_labels=True, font_color='black', verticalalignment='center', horizontalalignment='center', width=1, linewidths=1, node_size=500, alpha=0.8, labels={node: node for node in G.nodes()})
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    #############################
    # SAMPLE. The edges will be given as input (variable 'graph_state' needs to be a list of edges for the graph state).
    
    edge_labels_gs = {}
    for node in nodes.values():
        edge_gs = (node._name, 'Jussieu')
        # edge_labels_gs[edge_gs] = '%g km'%node._dist # there is no distance in this case
    ##############################
    
    # Terminar esto:
    if graph_state:
        GS = nx.graph()
        for node in nodes.values():
            GS.add_edge(node._name, 'Jussieu')
        
        nx.draw_networkx_edges(GS, pos, edge_color='purple')
    
    # sm = plt.cm.ScalarMappable(norm=None, cmap=cmap)
    # plt.colorbar(sm, orientation='vertical', shrink=0.8, label=r'Distance to nearest Qonnector [km]')
    
    plt.show()
    save_dir = 'plots'
    aux.check_dir(save_dir)
    plt.savefig(save_dir + os.sep + parameters['network'] +'.png')


if __name__ == "__main__":
    
    from GHZ_network import Node
            
    parameters = aux.read_parameters('parameters')
    parameters['network'] = 'QEurope'
    
    network = pd.read_csv('networks' + os.sep + parameters['network'] + '.csv', header=0)
    
    nodes = {}
    for n in range(len(network)):
        nodes[network['Name'].at[n]] = Node(network['Name'].at[n], network['Link'].at[n], network['Distance to Qonnector (km)'].at[n], network['Type'].at[n])

    N = nx.Graph()

    edges = list(zip(network['Name'], network['Link']))

    N.add_edges_from(edges)

    draw_network(N, nodes, parameters)
