#!/usr/bin/env python

#This file creates a local network with one Qonnector and 4 Qlient then simulates the creation and sending of a 
# 4 qubits GHZ state. The qubits received are stored in each Qlient's keylist.
# The output printed are the number of successful GHZ reception the rate and the QBER.

# PLOT = 0

import matplotlib.pyplot as plt
from QEuropeFunctions import *

# Simulation time
# simtime = 100000

ns.sim_reset()
# Creation of a network instance
net2 = QEurope("net")

# Qonnector
q = "Qonnector_1"
net2.Add_Qonnector(q)

# Nodes
N_nodes = 5 # Number of nodes

#%%
class Node:
    def __init__(self, node_name, dist_to_Qonnector, node_type):
        self.name = node_name
        self.dist = dist_to_Qonnector
        self.type = node_type # processor, etc. Not used yet.

nodes = {}

nodes[q] = Node(q, 0, 'Qonnector') # Qonnector.

for n in range(N_nodes):
    nodes[n] = Node('node_%s'%str(n), 10*n, 'node') # distances d=10*n, for now.
    
    net2.Add_Qlient(nodes[n].name, nodes[n].dist, q) # Connections between the parties and the Qonnector

#%%
# Visualisation of the network.

import networkx as nx
G = nx.Graph()

elist = []

# Adding edges between the nodes and the Qonnector
for n in range(N_nodes):
    elist.append((str(n), q))

G.add_edges_from(elist)

colours = []
for k in nodes.keys():
    colours.append(nodes[k].dist) # Value map for the colouring of the nodes.

cmap=plt.cm.summer
nx.draw(G, cmap=cmap,#plt.get_cmap('summer'),
        node_color=colours, with_labels=True, font_color='black', verticalalignment='center', horizontalalignment='center')



sm = plt.cm.ScalarMappable(cmap=cmap)#, norm=plt.Normalize(vmin = vmin, vmax=vmax))
sm._A = []
plt.colorbar(sm)


plt.show()

#%%

#Initialisation of the nodes
net = net2.network
Qonnector=net.get_node("Qonnector")

# Alice = net.get_node("node_Alice")
# Bob = net.get_node("node_Alice")
# Charlie = net.get_node("Jussieu")
# Dina = net.get_node("IRIF")

# Alice.keylist=[]
# Bob.keylist=[]
# Charlie.keylist=[]
# Dina.keylist=[]

# #Initialisation of the protocol
# GHZProtocol = SendGHZ4(Alice, Bob, Charlie, Dina, GHZ4_succ, Qonnector)
# GHZProtocol.start()

# protocolA = ReceiveProtocol(Qonnector, Qlient_meas_succ, Qlient_meas_flip, False, Alice)
# protocolA.start()

# protocolB = ReceiveProtocol(Qonnector, Qlient_meas_succ, Qlient_meas_flip, False, Bob)
# protocolB.start()

# protocolC = ReceiveProtocol(Qonnector, Qlient_meas_succ, Qlient_meas_flip, False, Charlie)
# protocolC.start() 
        
# protocolD = ReceiveProtocol(Qonnector, Qlient_meas_succ, Qlient_meas_flip,False, Dina)
# protocolD.start()

# #Simulation starting
# stat = ns.sim_run(duration=simtime)

# #Adding dark count for each Qlient
# addDarkCounts(Alice.keylist, pdarkworst, int(simtime/GHZ4_time))
# addDarkCounts(Bob.keylist, pdarkworst, int(simtime/GHZ4_time))
# addDarkCounts(Charlie.keylist, pdarkbest, int(simtime/GHZ4_time))
# addDarkCounts(Dina.keylist, pdarkbest, int(simtime/GHZ4_time))

# #Sifting to keep the qubit from the same GHZ state
# Lres=Sifting4(Alice.keylist,Bob.keylist,Charlie.keylist,Dina.keylist)



# print("Number of qubits received by the four Qlients: " +str(len(Lres)) )
# print("GHZ4 sharing rate : " + str(len(Lres)/(simtime*1e-9))+" GHZ4 per second")

# print("QBER : "+str(estimQBERGHZ4(Lres)))

