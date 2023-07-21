#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 15:25:24 2023

@author: santiago
"""

# Small network example.

import netsquid as ns
import numpy as np
# import pandas as pd
# import os

# import QEuropeFunctions as qe
# import aux
# import networkx as nx
# import quantum_networks_functions as qnf

#%%

def qonnect(Q):
    # This function takes a Qonnector Q that shares Bell pairs with all its Qlients 
    # and returns them sharing a GHZ state.
    return

#%%

def print_Q():
    # q=Q[0]
    # print('\n')
    print(Q[0].qstate.qrepr)

def combine_Q(Q):
    for q in Q[1:]:
        Q[0].combine(q)

n_qubits = 4

import itertools

basis = list(itertools.product([0, 1], repeat=n_qubits))

def print_state():
    coefficients = [np.round(x[0],3) for x in Q[0].qstate.qrepr.ket]
    # '+'.join(list(map(str, zip(coefficients, basis))))
    state = ''
    for c,b in zip(coefficients, basis):
        if c:
            state = state + ' + ' + str(c) + '\t| %s >'%str(b).strip('()') + '\n'
    print(state)

#%%

Q = ns.qubits.create_qubits(n_qubits)
combine_Q(Q)
# print_Q()
print_state()

qmem = ns.components.qmemory.QuantumMemory('MyQMem', num_positions=len(Q))
qmem.put(Q)

print('H on q0')
ns.components.instructions.INSTR_H(qmem, positions=[0])
# print_Q()
print_state()

print('CNOT on q0 & q1')
ns.components.instructions.INSTR_CNOT(qmem, positions=[0,1])
# print_Q()
print_state()

print('H on q2')
ns.components.instructions.INSTR_H(qmem, positions=[2])
# print_Q()
print_state()

print('CNOT on q2 & q3')
ns.components.instructions.INSTR_CNOT(qmem, positions=[2, 3])
# print_Q()
print_state()

#%%

# measurement_result, prob = ns.qubits.measure(qubit, observable=ns.X)

print('X measurement on q1 ')
ns.components.instructions.INSTR_H(qmem, positions=[2])
# print_Q()
print_state()


# print('H on q2')
# ns.components.instructions.INSTR_H(qmem, positions=[2])
# # print_Q()
# print_state()

# # TODO: fix from here on.
# print('CNOT on q1 & q2')
# ns.components.instructions.INSTR_CNOT(qmem, positions=[1, 2])
# # print_Q()
# print_state()

#%%
'''
#graph way

Q = ns.qubits.create_qubits(4)
print_Q()

combine_Q(Q)
print_Q()

qmem = ns.components.qmemory.QuantumMemory('MyQMem', num_positions=len(Q))
qmem.put(Q)

print('H on q0')
ns.components.instructions.INSTR_H(qmem, positions=[0])

print('H on q1')
ns.components.instructions.INSTR_H(qmem, positions=[1])

print('H on q2')
ns.components.instructions.INSTR_H(qmem, positions=[2])

print('H on q3')
ns.components.instructions.INSTR_H(qmem, positions=[3])
print_Q()

#create star graph with central node 1
print('CZ on q0 & q1')
ns.components.instructions.INSTR_CZ(qmem, positions=[0,1])
print_Q()

print('CZ on q1 & q2')
ns.components.instructions.INSTR_CZ(qmem, positions=[1,2])
print_Q()

print('CZ on q1 & q3')
ns.components.instructions.INSTR_CZ(qmem, positions=[1,3])
print_Q()

#hadamard on everything but 1 to get star to ghz
print('H on q0')
ns.components.instructions.INSTR_H(qmem, positions=[0])
print_Q()

print('H on q2')
ns.components.instructions.INSTR_H(qmem, positions=[2])
print_Q()

print('H on q3')
ns.components.instructions.INSTR_H(qmem, positions=[3])
print_Q()

#%%

#graph way

Q = ns.qubits.create_qubits(4)
print_Q()

combine_Q(Q)
print_Q()

qmem = ns.components.qmemory.QuantumMemory('MyQMem', num_positions=len(Q))
qmem.put(Q)

print('H on q0')
ns.components.instructions.INSTR_H(qmem, positions=[0])

print('H on q1')
ns.components.instructions.INSTR_H(qmem, positions=[1])

print('H on q2')
ns.components.instructions.INSTR_H(qmem, positions=[2])

print('H on q3')
ns.components.instructions.INSTR_H(qmem, positions=[3])
print_Q()

#create line graph
print('CZ on q0 & q1')
ns.components.instructions.INSTR_CZ(qmem, positions=[0,1])
print_Q()

print('CZ on q1 & q2')
ns.components.instructions.INSTR_CZ(qmem, positions=[1,2])
print_Q()

print('CZ on q2 & q3')
ns.components.instructions.INSTR_CZ(qmem, positions=[2,3])
print_Q()




#print(ns.qubits.qrepr.QRepr(2))

# print(ns.qubits.qstate.QState.qrepr)

# dm1 = ns.qubits.dmtools.DenseDMRepr(num_qubits=2)
# print(dm1)

# # ns.qubits.combine_qubits([q1, q2])
# ns.qubits.measure(q2, discard=True)


# %%
# class Network():
#     def __init__(self, node_name, qonnector, dist_to_Qonnector, node_type):
        
# class Node:
#     def __init__(self, node_name, link, dist_to_Qonnector, node_type):
#         self._name = node_name
#         self._link = link # Hub the node is connected to.
#         self._dist = dist_to_Qonnector
#         self._type = node_type # Qonnector, Qlient.
#         self._keylist = []   # shared one-time pad

# %%

# parameters = aux.read_parameters('parameters')
# parameters['network'] = 'QEurope'

# network = pd.read_csv('networks' + os.sep + parameters['network'] + '.csv', header=0)

# flags = {'draw_network': 1,
#          'print_parameters': 0,
#          'save_parameters': 0,
#          'print_lists': 1,
#          'save_results': 0,
#          'runtimes': 0,
#          }

# if flags['print_parameters']:
#     print('\n', parameters, '\n')

# if flags['save_parameters']:
#     directory = 'previous_parameters'
#     aux.check_dir(directory)
#     aux.save_parameters(directory)

# if flags['runtimes']:
#     import time
#     start = time.time()

# nodes = {}

# for n in range(len(network)):
#     nodes[network['Name'].at[n]] = Node(network['Name'].at[n], network['Link'].at[n], network['Distance to Qonnector (km)'].at[n], network['Type'].at[n])

# ns.sim_reset()

# # Creation of a network instance
# net2 = qnf.QEurope("net")

# # Initialisation of the nodes
# net = net2.network

# # Qonnector
# Qonnectors = []
# Qlients = []

# for node in nodes.values():
#     if node._type == 'Qonnector':
#         net2.Add_Qonnector(node._name)
#         Qonnectors.append(net.get_node(node._name))
#     elif node._type == 'Qlient':
#         net2.Add_Qlient(node._name, node._dist, node._link)
#         Qlients.append(net.get_node(node._name))
#     else:
#         print('Unknown node type: "%s" for node "%s". Nodes must be either of type "Qonnector" or "Qlient".'%(node._type, node._name))
        
# if flags['draw_network']:
#     G = nx.Graph()

#     edges = list(zip(network['Name'], network['Link']))

#     G.add_edges_from(edges)

#     qnf.draw_network(G, nodes, parameters)

# # %%

# for q in Qonnectors:
#     ghzprotocol = qnf.send_ghz(Qlients, parameters, q)  # THIS LINE IS WRONG. THE GHZ STATE SHOULD BE DISTRIBUTED ONLY TO THE NODES LINKED TO THE QONNECTOR q, NOT TO ALL QLIENTS.
#     print('Check this line.')

# ghzprotocol.start()

# protocols = []
# for node in nodes:
#     protocols.append(qe.ReceiveProtocol(Qonnectors, qe.Qlient_meas_succ, qe.Qlient_meas_flip, False, Qlients[node.name]))
#     protocols[node.name].start()

# # Simulation starting
# stat = ns.sim_run(duration=parameters['simtime'])

# # Adding dark count for each Qlient
# for node in nodes:
#     qe.addDarkCounts(Qlients[node.name].keylist, parameters['DCRateWorst'] * parameters['DetectGateWorst'],
#                      int(parameters['simtime'] / parameters['ghz_time']))

# #%% Sifting.

# LISTS = qnf.sifting(nodes, Qlients) # Sifting to keep the qubit from the same GHZ state


# if flags['print_lists']:
#     print("\nNumber of qubits received by the %d Qlients: %d" % (len(nodes), len(LISTS)))

#     print(LISTS)
#     # print("QBER:\t%g" % qe.estimQBERGHZ4(Lres))

# if flags['save_results']:
#     print('TODO: save_results')

# if flags['runtimes']:
#     end = time.time()
#     print('Elapsed time:\t%d\tseconds'%(end-start))
'''