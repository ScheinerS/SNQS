#!/usr/bin/env python

#This file creates a local network with one Qonnector and 4 Qlient then simulates the creation and sending of a 
# 4 qubits GHZ state. The qubits received are stored in each Qlient's keylist.
# The output printed are the number of successful GHZ reception the rate and the QBER.

# PLOT = 0

import matplotlib.pyplot as plt
from QEuropeFunctions import * 

#Simulation time
# simtime = 100000

ns.sim_reset()
# Creation of a network instance
net2 = QEurope("net")

# Qonnector
q = "Qonnector_1" # name for the qonnector 1.
net2.Add_Qonnector(q)

# Nodes
N_nodes = 5 # Number of nodes

node_dist = {}

for n in range(N_nodes):
    node_dist[n] = 1 # all nodes at distance 1, to begin.

# node_dist = {1: 0.001, 2: 3.01} # distances from the node to the Qonnector

# Connections between the parties and the Qonnector
for n in node_dist.keys():
    net2.Add_Qlient(str(n), 0.001, q)
    # net2.Add_Qlient("node_Bob", 3.01, q)

# net2.Add_Qlient("Telecom",18.77,"QonnectorParis")
# net2.Add_Qlient("Chatillon",6.77,"QonnectorParis")
# net2.Add_Qlient("CEA",31.35,"QonnectorParis")

#%%
# Visual representation of the network.

import networkx as nx
G = nx.Graph()

# elist = [('Alice', 'Qonnector'), ('Bob', 'Qonnector')]

elist = []
# Adding edges between the nodes and the Qonnector
for n in node_dist.keys():
    elist.append((str(n), q))

G.add_edges_from(elist)

# Value map for the colouring of the nodes:
val_map = {q: 1.0}#,
           # 'D': 0.5714285714285714,
           # 'H': 0.0}

values = [val_map.get(node, 0.25) for node in G.nodes()]

nx.draw(G, cmap=plt.get_cmap('summer'), node_color=values, with_labels=True, font_color='black', verticalalignment='bottom')
plt.show()

#%%


# #Initialisation of the nodes
# net = net2.network
# Qonnector=net.get_node("QonnectorParis")

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

