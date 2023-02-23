#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:29:57 2023

@author: santiago
"""

import networkx as nx

G = nx.Graph()

elist = [(1, 2), (2, 3), (1, 4), (4, 2)]
G.add_edges_from(elist)

nx.draw(G)

print(nx.adjacency_matrix(G))