#!/usr/bin/env python

# This file creates a local network with one Qonnector and 4 Qlient then simulates the creation and sending of a 4 qubits GHZ state. The qubits received are stored in each Qlient's keylist.
# The output printed are the number of successful GHZ reception the rate and the QBER.

# PLOT = 0

import numpy as np
import netsquid as ns
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# from QEuropeFunctions import *
import QEuropeFunctions as qe
import quantum_networks_functions as qnf

plt.rcParams['text.usetex'] = True

# Simulation time


ns.sim_reset()
# Creation of a network instance
net2 = qe.QEurope("net")

# Qonnector
q = "Qonnector 1"
net2.Add_Qonnector(q)

DRAW_NETWORK = 0
SIFTING = 1 # TO BE REMOVED ONCE IT'S GENERALISED TO N NODES.

#%%

P = pd.read_csv('parameters.csv', header=0)
P['value'] = pd.to_numeric(P['value'], downcast='integer', errors='ignore')
parameters = dict(zip(P['parameter'], P['value']))

N_nodes = int(parameters['N_nodes'])

#%%
class Node:
    def __init__(self, node_name, dist_to_Qonnector, node_type):
        self.name = node_name
        self.dist = dist_to_Qonnector
        self.type = node_type # processor, etc. Not used yet.

nodes = {}

nodes[q] = Node(q, 0, 'Qonnector') # Qonnector.

for n in range(N_nodes):
    nodes[n] = Node('node_%s'%str(n), n, 'node') # distances d=n, for now.
    
    net2.Add_Qlient(nodes[n].name, nodes[n].dist, q) # Connections between the parties and the Qonnector

#%%
# Visualisation of the network.

G = nx.Graph()

elist = []

# Adding edges between the nodes and the Qonnector
for n in range(N_nodes):
    elist.append((str(n), q))

G.add_edges_from(elist)

if DRAW_NETWORK:
    qnf.draw_network(G, nodes)

#%%

# Here starts the GHZ distribution protocol. For now, it works only for four nodes.

# Initialisation of the nodes
net = net2.network

Qonnector = net.get_node(q)

Qlients = []
for n in range(N_nodes):
    Qlients.append(net.get_node("node_%d"%n))
    Qlients[n].keylist=[]

# Initialisation of the protocol

ghzprotocol = qnf.send_ghz(Qlients, parameters, Qonnector)

ghzprotocol.start()

protocols = []
for n in range(N_nodes):
    protocols.append(qe.ReceiveProtocol(Qonnector, qe.Qlient_meas_succ, qe.Qlient_meas_flip, False, Qlients[n]))
    protocols[n].start()

#Simulation starting
stat = ns.sim_run(duration=parameters['simtime'])

#Adding dark count for each Qlient
for n in range(N_nodes):
    qe.addDarkCounts(Qlients[n].keylist, parameters['DCRateWorst']*parameters['DetectGateWorst'], int(parameters['simtime']/parameters['ghz_time']))

#%%

# Lists for each node.

LISTS = pd.DataFrame()
LISTS['time'] = None

for n in range(N_nodes):
    # n=1
    col = '%s_measurement'%nodes[n].name
    LISTS[col] = None
    df = pd.DataFrame(columns=['time', col])
    
    for (time, measurement) in  Qlients[n].keylist:
        new_line = pd.DataFrame({'time': time, col: [measurement]})
        df = pd.concat([df, new_line])

    LISTS = LISTS.merge(df, how='outer')

#%%

#Sifting to keep the qubit from the same GHZ state
if SIFTING:
    if N_nodes==3:
        Lres = qe.Sifting3(Qlients[0].keylist, Qlients[1].keylist, Qlients[2].keylist)
    elif N_nodes==4:
        Lres = qe.Sifting4(Qlients[0].keylist, Qlients[1].keylist, Qlients[2].keylist, Qlients[3].keylist)
    elif N_nodes==5:
        Lres = qe.Sifting5(Qlients[0].keylist, Qlients[1].keylist, Qlients[2].keylist, Qlients[3].keylist, Qlients[4].keylist)
    
    print("Number of qubits received by the %d Qlients: %d"%(N_nodes, len(Lres)) )
    print("Sharing rate : " + str(len(Lres)/(parameters['simtime']*1e-9)) +" GHZ states per second")
    
    print("QBER : " + str(qe.estimQBERGHZ4(Lres)))
