#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 12:06:56 2023

@author: santiago
"""

import matplotlib.pyplot as plt
import networkx as nx

plt.close('all')

# G = nx.cubical_graph()

n = 8

G = nx.star_graph(n, create_using=None)

pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes

type_A = [1, 4, 5]
type_B = [2, 3, 6, 7, 8]

# nodes
options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9}
nx.draw_networkx_nodes(G, pos, nodelist=[0], node_color="grey", **options)
nx.draw_networkx_nodes(G, pos, nodelist = type_A, node_color="tab:red", **options)
nx.draw_networkx_nodes(G, pos, nodelist = type_B, node_color="tab:blue", **options)

# edges
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

'''
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
    width=8,
    alpha=0.5,
    edge_color="tab:red",
)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
    width=8,
    alpha=0.5,
    edge_color="tab:blue",
)
'''

labels = {}
labels[0] = 'TTP'
for i in range(1, n+1):
    if i in type_A:
        labels[i] = r"$%d_{A}$"%i
    else:
        labels[i] = r"$%d_{B}$"%i

nx.draw_networkx_labels(G, pos, labels, font_size=15, font_color="black")

plt.tight_layout()
plt.axis("off")
plt.show()
plt.savefig('types_A_and_B.png')
