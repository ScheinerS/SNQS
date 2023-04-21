#!/usr/bin/env python

# import matplotlib.pyplot as plt
# import numpy as np
import netsquid as ns
import pandas as pd
import os

import QEuropeFunctions as qe
import aux
import networkx as nx
import quantum_networks_functions as qnf

# %%
# class Network():
#     def __init__(self, node_name, qonnector, dist_to_Qonnector, node_type):
        
class Node:
    def __init__(self, node_name, link, dist_to_Qonnector, node_type):
        self._name = node_name
        self._link = link # Hub the node is connected to.
        self._dist = dist_to_Qonnector
        self._type = node_type # Qonnector, Qlient.
        self._keylist = []   # shared one-time path

#%%

parameters = aux.read_parameters('parameters.csv')

aux.read_network(parameters['network'])
network = pd.read_csv('networks' + os.sep + parameters['network'] + '.csv', header=0)

flags = {'draw_network': 1,
         'print_parameters': 0,
         'save_parameters': 0,
         'print_lists': 1,
         'save_results': 0,
         'runtimes': 0,
         }

if flags['print_parameters']:
    print('\n', parameters, '\n')

if flags['save_parameters']:
    directory = 'previous_parameters'
    aux.check_dir(directory)
    aux.save_parameters(directory)

if flags['runtimes']:
    import time
    start = time.time()

nodes = {}

# Qonnectors
# for q in network[network['Type']=='Qonnector']['Name']:
#     nodes[q] = Node(q, None, 0, 'Qonnector')

for n in range(len(network)):
    nodes[network['Name'].at[n]] = Node(network['Name'].at[n], network['Link'].at[n], network['Distance to Qonnector (km)'].at[n], network['Type'].at[n])

ns.sim_reset()

# Creation of a network instance
net2 = qnf.QEurope("net")

# Initialisation of the nodes
net = net2.network

# Qonnector
Qonnectors = []
Qlients = []

for node in nodes.values():
    if node._type == 'Qonnector':
        net2.Add_Qonnector(node._name)
        Qonnectors.append(net.get_node(node._name))
    elif node._type == 'Qlient':
        net2.Add_Qlient(node._name, node._dist, node._link)
        Qlients.append(net.get_node(node._name))
    else:
        print('Unknown node type: "%s" for node "%s". Nodes must be either of type "Qonnector" or "Qlient".'%(node._type, node._name))
        
if flags['draw_network']:
    G = nx.Graph()

    edges = list(zip(network['Name'], network['Link']))

    G.add_edges_from(edges)

    qnf.draw_network(G, nodes, parameters)

# %%

for q in Qonnectors:
    ghzprotocol = qnf.send_ghz(Qlients, parameters, q)  # THIS LINE IS WRONG. THE GHZ STATE SHOULD BE DISTRIBUTED ONLY TO THE NODES LINKED TO THE QONNECTOR q, NOT TO ALL QLIENTS.
    print('Check this line.')

ghzprotocol.start()

protocols = []
for node in nodes:
    protocols.append(qe.ReceiveProtocol(Qonnectors, qe.Qlient_meas_succ, qe.Qlient_meas_flip, False, Qlients[node.name]))
    protocols[node.name].start()

# Simulation starting
stat = ns.sim_run(duration=parameters['simtime'])

# Adding dark count for each Qlient
for node in nodes:
    qe.addDarkCounts(Qlients[node.name].keylist, parameters['DCRateWorst'] * parameters['DetectGateWorst'],
                     int(parameters['simtime'] / parameters['ghz_time']))

#%% Sifting.

LISTS = qnf.sifting(nodes, Qlients) # Sifting to keep the qubit from the same GHZ state


if flags['print_lists']:
    print("\nNumber of qubits received by the %d Qlients: %d" % (len(nodes), len(LISTS)))

    print(LISTS)
    # print("QBER:\t%g" % qe.estimQBERGHZ4(Lres))

if flags['save_results']:
    print('TODO: save_results')

if flags['runtimes']:
    end = time.time()
    print('Elapsed time:\t%d\tseconds'%(end-start))

#%%

# if __name__=='__main__':
#     print()