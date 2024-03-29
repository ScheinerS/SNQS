#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 15:25:24 2023

@author: santiago
"""

# Small network example.

import netsquid as ns
import numpy as np
import itertools

# import pandas as pd
# import os

# import QEuropeFunctions as qe
# import aux
# import networkx as nx
import quantum_networks_functions as qnf

# import ns.components.instructions.INSTR_CZ as CZ
#%%

# def qonnect(Q, verbose=1):
#     # This function takes a Qonnector Q that shares Bell pairs with all its Qlients 
#     # and returns them sharing a GHZ state.
#     return


def print_Q(Q):
    # q=Q[0]
    # print('\n')
    print(Q[0].qstate.qrepr)

def combine_Q(Q, verbose=0):
    if verbose:
        print(50*'*')
        print('Q:\n', Q[0].qstate.qrepr)
    for q in Q[1:]:
        Q[0].combine(q)
    if verbose:
        print('\nCombined Q\n:', Q[0].qstate.qrepr)
        print(50*'*')



# def print_state_as_ket(Q, print_format='plain', verbose=1):
    
#     # combine_Q(Q)
    
#     # n_qubits = len(Q)
#     # print('len(Q)=', len(Q))
    
#     basis = list(itertools.product([0, 1], repeat=len(Q)))
    
#     coefficients = [np.round(x[0],3) for x in Q[0].qstate.qrepr.ket]
#     # '+'.join(list(map(str, zip(coefficients, basis))))
#     state = ''
#     for c,b in zip(coefficients, basis):
#         # print(c, '\t', b)
#         # c=True # to print all coefficients.
#         if c:
#             if print_format=='plain':
#                 state = state + ' + ' + str(c).replace('+0j','').replace('-0j','') + '\t\t|%s>'%str(b).strip('()').replace(',', '') + '\n'
#             elif print_format=='latex':
#                 state = state + ' + ' + str(c).replace('+0j','').replace('-0j','') + ' \; \ket{%s}'%str(b).strip('()').replace(',', '') + ''
#             else:
#                 state = state + ' + ' + str(c).replace('+0j','').replace('-0j','') + '\t| %s >'%str(b).strip('()').replace(',', '') + '\n'
    
#     if verbose:
#         print(state)
    
#     return state

def print_all_Qubits(Q):
    for i in range(len(Q)):
        coefficients = [np.round(x[0],3) for x in Q[i].qstate.qrepr.ket]
        print('Q[%d]:\n'%i, Q[i].qstate.qrepr.ket)
        print('\ncoefficients: ', coefficients, '\n\n')

# print_all_Qubits(Q)


def measure(qubit, observable, verbose=1):
    '''
    

    Parameters
    ----------
    qubit : TYPE
        DESCRIPTION.
    observable : TYPE
        DESCRIPTION.
    verbose : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    measurement_result : TYPE
        DESCRIPTION.
    prob : TYPE
        DESCRIPTION.

    '''
    
    '''
    
    ******************
    *** DO NOT USE ***
    ******************
    
    The measurement is apparently mixing the cubits after measurement.
    
    The resulting state is not what we should see, and the measured qubit seems
    to be always in position 0, instead of remaining in the original position.
    This happens every time, even if we control the list of qubits.
    
    '''
    
    QMEM = ns.components.qmemory.QuantumMemory('M', num_positions=1)
    QMEM.put(qubit)
    measurement_result, prob = QMEM.measure(positions=[0], observable=observable, discard=False)#, meas_operators=None, bool discard=False, bool skip_noise=False, bool check_positions=True)
    
    combine_Q(Q, verbose=0) # Measurements split the qubits, so they need to be combined again.
    
    if verbose:
        print(50*'-')
        print('Measurement of %s on %s'%(observable.name, qubit.name))
        print('Result:', measurement_result, 'with prob:', np.round(prob,3))
        print('Resulting state:')
        qnf.print_state_as_ket(Q, verbose=1) # TODO: Q no es argumento de la funcion.
        print(50*'-')

    return measurement_result, prob
#%%

if __name__=='__main__':
    # For a star graph of edges {(0,1), (1,2)} (i.e. the graph "0-1-2")
    
    d = 6
    n = 3
    
    Q = ns.qubits.create_qubits(d)
    combine_Q(Q)
    
    qmem = ns.components.qmemory.QuantumMemory('MyQMem', num_positions=d)
    qmem.put(Q)
    
    print('\nInitial state:')
    qnf.print_state_as_ket(Q)
    # print_Q(Q)
    
    print('\nH on each qubit:')
    for i in range(d):
        ns.components.instructions.INSTR_H(qmem, positions=[i])
    
    qnf.print_state_as_ket(Q)

    if (d, n) == (4, 2):
        # 4-2 bundled graph state:
        ns.components.instructions.INSTR_CZ(qmem, positions=[0,2])
        ns.components.instructions.INSTR_CZ(qmem, positions=[0,3])
        ns.components.instructions.INSTR_CZ(qmem, positions=[1,2])
        ns.components.instructions.INSTR_CZ(qmem, positions=[1,3])

    elif (d, n) == (6, 2):
        # 6-2 bundled graph state:
        
        ns.components.instructions.INSTR_CZ(qmem, positions=[0,1])
        ns.components.instructions.INSTR_CZ(qmem, positions=[0,3])
        ns.components.instructions.INSTR_CZ(qmem, positions=[0,5])
    
        ns.components.instructions.INSTR_CZ(qmem, positions=[2,1])
        ns.components.instructions.INSTR_CZ(qmem, positions=[2,3])
        ns.components.instructions.INSTR_CZ(qmem, positions=[2,5])
    
        ns.components.instructions.INSTR_CZ(qmem, positions=[4,1])
        ns.components.instructions.INSTR_CZ(qmem, positions=[4,3])
        ns.components.instructions.INSTR_CZ(qmem, positions=[4,5])
        
    
    elif (d, n) == (6, 3):
        # 6-2 bundled graph state:
        ns.components.instructions.INSTR_CZ(qmem, positions=[0,2])
        ns.components.instructions.INSTR_CZ(qmem, positions=[0,3])
        ns.components.instructions.INSTR_CZ(qmem, positions=[0,4])
        ns.components.instructions.INSTR_CZ(qmem, positions=[0,5])
        
        ns.components.instructions.INSTR_CZ(qmem, positions=[1,2])
        ns.components.instructions.INSTR_CZ(qmem, positions=[1,3])
        ns.components.instructions.INSTR_CZ(qmem, positions=[1,4])
        ns.components.instructions.INSTR_CZ(qmem, positions=[1,5])
        
        ns.components.instructions.INSTR_CZ(qmem, positions=[2,4])
        ns.components.instructions.INSTR_CZ(qmem, positions=[2,5])
        ns.components.instructions.INSTR_CZ(qmem, positions=[3,4])
        ns.components.instructions.INSTR_CZ(qmem, positions=[3,5])
        

    
    qnf.print_state_as_ket(Q)
    
    # measurement_result, prob = measure(Q[0], ns.Z)
    # measurement_result, prob = measure(Q[0], ns.X)

    
    # print(qmem.peek(positions=[0])[0].qstate.qrepr.ket)
    # measurement_result, prob = qmem.measure(positions=[0], observable=ns.Z, discard=False)#, meas_operators=None, bool discard=False, bool skip_noise=False, bool check_positions=True)
    # print(qmem.peek(positions=[0])[0].qstate.qrepr.ket)
    
    # print_all_Qubits(Q)
    
    # measurement_result, prob = measure(Q[1], ns.Z)
    # print_state_as_ket(Q, verbose=1)
    
    '''
    # print('H on q3 (Qonnector)')
    # ns.components.instructions.INSTR_H(qmem, positions=[3])
    # print_state_as_ket(Q, verbose=1)
    
    print('CNOT')
    ns.components.instructions.INSTR_CZ(qmem, positions=[0,1])
    ns.components.instructions.INSTR_CZ(qmem, positions=[1,2])
    ns.components.instructions.INSTR_CZ(qmem, positions=[2,3])
    print_state_as_ket(Q, verbose=1)
    
    
    print('Measurement on q1')
    measurement_result, prob = qmem.measure(positions=[1], observable=ns.X, discard=True)#, meas_operators=None, bool discard=False, bool skip_noise=False, bool check_positions=True)
    # measurement_result, prob = ns.qubits.measure(Q[1], observable=ns.Z)
    # measurement_result, prob = ns.qubits.measure(Q[1], observable=ns.Z)
    print('Result:', measurement_result, 'with prob:', np.round(prob,3), '\n')
    print_state_as_ket(Q, verbose=1)

    # ns.components.instructions.INSTR_H(qmem, positions=[1])
    #%%
    print('Rotation in y')
    Rotation_y = ns.components.instructions.IRotationGate('Rotation_y')
    if measurement_result==0:
        ns.components.instructions.INSTR_H(qmem, positions=[0])
        # Rotation_y.execute(qmem, positions=[1],angle=np.pi/4, axis=(0,1,0))
        # ns.components.instructions.INSTR_Z(qmem, positions=[2])
    else:
        ns.components.instructions.INSTR_X(qmem, positions=[0])
        ns.components.instructions.INSTR_H(qmem, positions=[0])
        # Rotation_y.execute(qmem, positions=[1],angle=(-1)*np.pi/4, axis=(0,1,0))
        # ns.components.instructions.INSTR_Z(qmem, positions=[0])
        
    # ns.components.instructions.INSTR_CZ(qmem, positions=[1,2])     
    print_state_as_ket(Q, verbose=1)
    
    
    # print('CNOT on q1 & q2')
    # ns.components.instructions.INSTR_CNOT(qmem, positions=[1,2])
    # print_state_as_ket(Q, verbose=1)
    
    # print('CNOT on q3 & q2')
    # ns.components.instructions.INSTR_CNOT(qmem, positions=[3,2])
    # print_state_as_ket(Q, verbose=1)

        
    #%%
    
    # measurement_result, prob = ns.qubits.measure(qubit, observable=ns.X)
    
    # print('X measurement on q1 ')
    # ns.components.instructions.INSTR_H(qmem, positions=[2])
    # # print_Q()
    # print_state_as_ket(Q)
    
    
    # print('H on q2')
    # ns.components.instructions.INSTR_H(qmem, positions=[2])
    # # print_Q()
    # print_state()
    
    # # TODO: fix from here on.
    # print('CNOT on q1 & q2')
    # ns.components.instructions.INSTR_CNOT(qmem, positions=[1, 2])
    # # print_Q()
    # print_state()
    '''
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