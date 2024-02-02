#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2023
@author: Santiago Scheiner

Protocols from: "Shettell, Hassani, Markham - Private network parameter estimation with quantum sensors"
"""

# import netsquid as ns
# import pandas as pd
# import os

import numpy as np
# import QEuropeFunctions as qe
# import aux
# import networkx as nx
# import quantum_networks_functions as qnf
# import plot_network as pn
# import local_complementation as lc


#!/usr/bin/env python

#This file creates a local network with one Qonnector and 4 Qlient then simulates the creation and sending of a 
# 4 qubits GHZ state. The qubits received are stored in each Qlient's keylist.
# The output printed are the number of successful GHZ reception the rate and the QBER.
import netsquid as ns
# import matplotlib.pyplot as plt
# from QEuropeFunctions import * 

import netsquid.components.instructions as instr
# import netsquid.components.qprogram as qprog
# import numpy as np
# from netsquid.components import QuantumChannel, ClassicalChannel
from netsquid.components import QuantumMemory
# from netsquid.components.clock import Clock
# from netsquid.components.models.delaymodels import FixedDelayModel
# from netsquid.components.models.qerrormodels import FibreLossModel, DephaseNoiseModel
# from netsquid.components.qprocessor import PhysicalInstruction
# from netsquid.components.qprocessor import QuantumProcessor
# from netsquid.components.qsource import QSource, SourceStatus
from netsquid.nodes import Node
# from netsquid.nodes.network import Network
# from netsquid.protocols import NodeProtocol
# from netsquid.qubits import ketstates as ks
# from netsquid.qubits.dmtools import DenseDMRepr
# from netsquid.qubits.state_sampler import StateSampler
# from scipy.stats import bernoulli
from netsquid.qubits.qubit import Qubit

from quantum_networks_functions import print_state_as_ket, combine_qubits
# class Node(Node):
#     def __init__(self, node_name, links, dist_to_Qonnector, node_type, number_of_qubits=1):
#         self._name = node_name
#         self._links = links # List of neighbours.
#         self._dist = dist_to_Qonnector
#         self._type = node_type # Qonnector, Qlient.
#         self._keylist = []   # shared one-time pad
#         self._number_of_qubits = number_of_qubits   # number of qubits for this node
#         self._qubits = ns.qubits.create_qubits(number_of_qubits)





#%%



def verification(Q, PRINT_K: bool=False, PRINT_STABILISERS_ON_STATE: bool=False, v: bool=False):
    '''
    Protocol 1 ('Verification') for a list of qubits 'Q'.


    Parameters
    ----------
    Q : list
        list of qubits to perform the verification on.
    PRINT_K : bool, optional
        whether to print the stabilisers 'K'. The default is True.
    PRINT_STABILISERS_ON_STATE : bool, optional
        whether to apply the stabilisers 'K' on the states. The default is True.
    v : bool, optional
        whether to print the effect of the stabilisers step by step. The default is True.


    Returns
    -------
    None.
    '''
    
    
    n_qubits = len(Q)
    mY = ns.qubits.operators.Operator('-Y', -1*ns.Y)
    
    K = {}
    for i in range(n_qubits):
        operators = [mY, ns.Y]
        for j in range(n_qubits-2):
            operators.append(ns.X)
    
        K[i] = list(np.roll(operators, i))
    
    
    '''
    I think in the paper 'K_{n+1}' is missing.
    '''
    K[n_qubits] = [ns.X]
    for j in range(n_qubits-1):
        K[n_qubits].append(ns.X)
    
    PRINT_K = 1
    if PRINT_K:
        for key in K.keys():
            print('\nK[%d]:\t'%key, end='')
            for j in K[key]:
                print(j.name, end=' ')
        print('\n')
    
    if PRINT_STABILISERS_ON_STATE:
        for key in K.keys():
            print('\nK[%d]:\n'%key, end='')
            if v:
                print('Initial state:')
                print_state_as_ket(Q)
            for i in range(len(K[key])):
                if v:
                    print(K[key][i].name, 'on qubit', i)
                qmem.operate(K[key][i], i)
                if v:
                    print_state_as_ket(Q)
                
            print(50*'-')
            # print_state_as_ket(Q)


    # TODO: include flag specifying if the state is correct, and rounds of verification.
    

#%%    
def secure_network_sensing(Q, Theta, v):
    '''
    

    Parameters
    ----------
    Q : TYPE
        DESCRIPTION.
    v : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    verification(Q)
    
    
    angle = np.pi/2
    
    
    if v:
        print('Before rotation:')
        print_state_as_ket(Q)
    
    for i in range(len(Q)):
        R = ns.qubits.operators.create_rotation_op(angle, rotation_axis=(0, 0, 1))
        qmem.operate(R, i)
    if v:
        print('After rotation:')
        print_state_as_ket(Q)
    
    
    
    # Encoding:
    for node_i in range(len(Q)):
        # TODO: To be replaced with: for node in nodes.values().
        
        ns.components.instructions.IRotationGate('encode', axis=None, controlled=False, check_standard_rotations=True, angle_precision=8)
        
        '''
        NO. ESE COMANDO ES PARA 90, 180, 270. DEFINIR NUEVA ROTACION.
        '''
# print('Node %2d measures X:'%0)
'''
m, p = qmem.measure(positions=[1], observable=ns.Y)
print_state_as_ket(Q)
m, p = qmem.measure(positions=[2], observable=ns.X)
print_state_as_ket(Q)

combine_qubits(Q, v=True)
print_state_as_ket(Q)
'''
# [qmem.measure(positions=[i], observable=ns.X) for i in range(n_qubits)]

# print('Q[0]:\n', Q[0].qstate.qrepr.ket)

# print('Q[0]:\n', Q[0].qstate.qrepr.ket)

# [qmem.measure(positions=[i], observable=ns.Z) for i in range(len(Q))]


#%%

if __name__=='__main__':
        
    # Creation of n qubits:
    n_qubits = 3

    Q = ns.qubits.create_qubits(n_qubits)
    
    Theta = {}
    for node_name in range(len(Q)):
        # TODO: 'node_name' can be converted to 'node._name' later.
        Theta[node_name] = node_name*np.pi/2 # TODO: Finish this.
        # For now, node 0 encodes '0 deg', node 1 encodes '10 deg', etc.
        
    qmem = QuantumMemory('QM', num_positions=len(Q))
    qmem.put(Q)

    # GHZ state:
    instr.INSTR_H(qmem, positions=[0])
    for i in range(1, n_qubits):
        instr.INSTR_CNOT(qmem, positions=[0, i])

    print('Initial GHZ state:')
    print_state_as_ket(Q)
    # print('Q[0]:\n', Q[0].qstate.qrepr.ket)
    secure_network_sensing(Q, Theta, v=0)