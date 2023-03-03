#!/usr/bin/env python

# This file creates a local network with one Qonnector and 4 Qlient then simulates the creation and sending of a 4 qubits GHZ state. The qubits received are stored in each Qlient's keylist.
# The output printed are the number of successful GHZ reception the rate and the QBER.

# PLOT = 0

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import netsquid as ns

from QEuropeFunctions import *
import quantum_networks_functions as qnf

plt.rcParams['text.usetex'] = True

# Simulation time
simtime = 1e5

ns.sim_reset()
# Creation of a network instance
net2 = QEurope("net")

# Qonnector
q = "Qonnector 1"
net2.Add_Qonnector(q)

# Nodes
N_nodes = 4 # Number of nodes

#%%
class Node:
    def __init__(self, node_name, dist_to_Qonnector, node_type):
        self.name = node_name
        self.dist = dist_to_Qonnector
        self.type = node_type # processor, etc. Not used yet.

nodes = {}

nodes[q] = Node(q, 0, 'Qonnector') # Qonnector.

for n in range(N_nodes):
    nodes[n] = Node('node_%s'%str(n), n/10, 'node') # distances d=10*n, for now.
    
    net2.Add_Qlient(nodes[n].name, nodes[n].dist, q) # Connections between the parties and the Qonnector

#%%
# Visualisation of the network.

plt.close('all')

G = nx.Graph()

elist = []

# Adding edges between the nodes and the Qonnector
for n in range(N_nodes):
    elist.append((str(n), q))

G.add_edges_from(elist)

colours = []
for k in nodes.keys():
    colours.append(nodes[k].dist) # Value map for the colouring of the nodes.

cmap=plt.cm.coolwarm

node_positions = {} # pos (dict or None optional (default=None)) – Initial positions for nodes as a dictionary with node as keys and values as a coordinate list or tuple. If None, then use random initial positions.
for k in nodes.keys():
    node_positions[k] = (np.sqrt(nodes[k].dist), np.sqrt(nodes[k].dist))

nx.draw(G, cmap=cmap, node_color=colours, with_labels=True, font_color='black', verticalalignment='center', horizontalalignment='center')


sm = plt.cm.ScalarMappable(cmap=cmap)#, norm=plt.Normalize(vmin = vmin, vmax=vmax))
sm._A = []
plt.colorbar(sm, orientation='vertical', shrink=0.8, label=r'Distance to Qonnector')


plt.show()

#%%

# Here starts the GHZ distribution protocol. For now, it works only for four nodes.

#Initialisation of the nodes
net = net2.network

Qonnector = net.get_node(q)

Qlients = []
for n in range(N_nodes):
    Qlients.append(net.get_node("node_%d"%n))
    Qlients[n].keylist=[]

# Initialisation of the protocol

ghzprotocol = qnf.send_ghz(Qlients, GHZ4_succ, Qonnector)
# ghzprotocol = qnf.send_ghz(Qlients[0], Qlients[1], Qlients[2], Qlients[3], GHZ4_succ, Qonnector)
# ghzprotocol = SendGHZ4(Qlients[0], Qlients[1], Qlients[2], Qlients[3], GHZ4_succ, Qonnector)

ghzprotocol.start()

protocols = []
for n in range(N_nodes):
    protocols.append(ReceiveProtocol(Qonnector, Qlient_meas_succ, Qlient_meas_flip, False, Qlients[n]))
    protocols[n].start()

#Simulation starting
stat = ns.sim_run(duration=simtime)

#Adding dark count for each Qlient
for n in range(N_nodes):
    addDarkCounts(Qlients[n].keylist, pdarkworst, int(simtime/GHZ4_time))


#Sifting to keep the qubit from the same GHZ state
Lres=Sifting4(Qlients[0].keylist, Qlients[1].keylist, Qlients[2].keylist, Qlients[3].keylist)

print("Number of qubits received by the four Qlients: " +str(len(Lres)) )
print("GHZ4 sharing rate : " + str(len(Lres)/(simtime*1e-9))+" GHZ4 per second")

print("QBER : "+str(estimQBERGHZ4(Lres)))
