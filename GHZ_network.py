#!/usr/bin/env python

# ctrl + alt + o : optimize imports

import matplotlib.pyplot as plt
# import numpy as np
import netsquid as ns
import pandas as pd

# from QEuropeFunctions import *
import QEuropeFunctions as qe
import aux
import networkx as nx
import quantum_networks_functions as qnf

# %%


plt.rcParams['text.usetex'] = True

ns.sim_reset()

# Creation of a network instance
net2 = qe.QEurope("net")

# Qonnector
q = "Qonnector 1"
net2.Add_Qonnector(q)

flags = {'draw_network': 0,
         'print_parameters': 1,
         'save_parameters': 0,
         'print_lists': 1,
         'save_results': 0,
         'runtimes': 0,
         }

    
if flags['runtimes']:
    import time
    start = time.time()

P = pd.read_csv('parameters.csv', header=0)
P['value'] = pd.to_numeric(P['value'], downcast='integer', errors='ignore')
parameters = dict(zip(P['parameter'], P['value']))

N_nodes = int(parameters['N_nodes'])


if flags['print_parameters']:
    print('\n', parameters, '\n')

if flags['save_parameters']:
    directory = 'previous_parameters'
    aux.check_dir(directory)
    aux.save_parameters(directory)

class Node:
    def __init__(self, node_name, dist_to_Qonnector, node_type):
        self.name = node_name
        self.dist = dist_to_Qonnector
        self.type = node_type # processor, etc. Not used yet.


nodes = {q: Node(q, 0, 'Qonnector')}

for n in range(N_nodes):
    nodes[n] = Node('node_%s' % str(n), n, 'node')  # distances d=n, for now.

    net2.Add_Qlient(nodes[n].name, nodes[n].dist, q)  # Connections between the parties and the Qonnector

# %% Visualisation of the network.

if flags['draw_network']:
    G = nx.Graph()

    elist = []

    # Adding edges between the nodes and the Qonnector
    for n in range(N_nodes):
        elist.append((str(n), q))

    G.add_edges_from(elist)

    qnf.draw_network(G, nodes)

# %%

# Initialisation of the nodes
net = net2.network

Qonnector = net.get_node(q)

Qlients = []
for n in range(N_nodes):
    Qlients.append(net.get_node("node_%d" % n))
    Qlients[n].keylist = []

ghzprotocol = qnf.send_ghz(Qlients, parameters, Qonnector)

ghzprotocol.start()

protocols = []
for n in range(N_nodes):
    protocols.append(qe.ReceiveProtocol(Qonnector, qe.Qlient_meas_succ, qe.Qlient_meas_flip, False, Qlients[n]))
    protocols[n].start()

# Simulation starting
stat = ns.sim_run(duration=parameters['simtime'])

# Adding dark count for each Qlient
for n in range(N_nodes):
    qe.addDarkCounts(Qlients[n].keylist, parameters['DCRateWorst'] * parameters['DetectGateWorst'],
                     int(parameters['simtime'] / parameters['ghz_time']))

#%% Sifting.

LISTS = qnf.sifting(nodes, Qlients) # Sifting to keep the qubit from the same GHZ state


if flags['print_lists']:
    print("\nNumber of qubits received by the %d Qlients: %d" % (N_nodes, len(LISTS)))

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