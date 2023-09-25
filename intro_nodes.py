#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 18:46:28 2023

@author: santiago
"""

#%% Exercise 111

import netsquid as ns
from netsquid.components.instructions import *
from netsquid.components import QuantumMemory


Q = ns.qubits.create_qubits(3)

qmem = QuantumMemory('QM', num_positions=len(Q))
qmem.put(Q)

INSTR_X(qmem, positions=[0])
INSTR_X(qmem, positions=[1])
INSTR_X(qmem, positions=[2])

print('Q[0]:\n', Q[0].qstate.qrepr.ket)
print('Q[1]:\n', Q[1].qstate.qrepr.ket)
print('Q[2]:\n', Q[2].qstate.qrepr.ket)


#%% Exercise +++

Q = ns.qubits.create_qubits(3)

qmem = QuantumMemory('QM', num_positions=len(Q))
qmem.put(Q)

INSTR_H(qmem, positions=[0])
INSTR_H(qmem, positions=[1])
INSTR_H(qmem, positions=[2])

print('Q[0]:\n', Q[0].qstate.qrepr.ket)
print('Q[1]:\n', Q[1].qstate.qrepr.ket)
print('Q[2]:\n', Q[2].qstate.qrepr.ket)

#%% Exercise GHZ

Q = ns.qubits.create_qubits(4)

qmem = QuantumMemory('QM', num_positions=len(Q))
qmem.put(Q)

INSTR_H(qmem, positions=[0])
INSTR_CNOT(qmem, positions=[0, 1])
INSTR_CNOT(qmem, positions=[1, 2])
INSTR_CNOT(qmem, positions=[2, 3])

print('Q[0]:\n', Q[0].qstate.qrepr.ket)

[qmem.measure(positions=[i], observable=ns.Z) for i in range(len(Q))]


#%%
# Nodes
from netsquid.components import QuantumChannel
from netsquid.nodes import Node
alice = Node("Alice")

print(alice)

from netsquid.components import QuantumMemory
qmemory = QuantumMemory("AliceMemory", num_positions=2)
alice.add_subcomponent(qmemory, name="memory1")
alice.subcomponents["memory1"]


bob = Node("Bob")

qmemory = QuantumMemory("BobMemory", num_positions=1)
bob.add_subcomponent(qmemory, name="memory1")
bob.subcomponents["memory1"]

alice.qmemory.ports['qout0']
alice.qmemory.ports['qout1']


#%% Channels

from netsquid.components import Channel, QuantumChannel
channel = QuantumChannel(name="Alice_to_Bob")

# channel.send(Q[0])

# ns.sim_run()

# items, delay = channel.receive()
# items
# delay

# ns.sim_reset()


#%% Ports

# We create a port for Alice:
alice.add_ports(['Alice_qout'])

# We connect the port qout1 of alice.qmemory with Alice_qout:
alice.qmemory.ports['qout'].forward_output(alice.ports['Alice_qout'])

# We create a port for Bob:
bob.add_ports(['Bob_qin'])

# We connect the port qout0 of bob.qmemory with Bob_qin:
bob.ports['Bob_qin'].forward_input(bob.qmemory.ports['qin'])

# alice.qmemory.ports["qout"].connect(alice.qchannel.ports["send"])
# alice.add_ports(['qin_charlie'])



channel.ports['send'].connect(alice.ports['Alice_qout'])
channel.ports['recv'].connect(bob.ports['Bob_qin'])

# Everything is now connected.

# To test it, we create one qubit and we put it in Alice's memory, in position '1':

Q = ns.qubits.create_qubits(2)

alice.qmemory.put(Q)

# So now Alice has the two qubits in her memory:
alice.qmemory.peek(0)
alice.qmemory.peek(1)

# And Bob has:
bob.qmemory.peek(0)

alice.qmemory.peek(0)
alice.qmemory.pop(1)

bob.qmemory.peek(0)

alice.qmemory.ports['qout'].forwarded_ports['output'].name
alice.ports['Alice_qout']
bob.ports['Bob_qin'].forwarded_ports['input'].name


#%% Entanglement swapping (without channels):

# Create Three nodes: Alice, Bob, and Charlie.

from netsquid.nodes import Node
alice = Node("Alice")

print(alice)

from netsquid.components import QuantumMemory
qmemory = QuantumMemory("AliceMemory", num_positions=2)
alice.add_subcomponent(qmemory, name="memory1")
alice.subcomponents["memory1"]


Q = ns.qubits.create_qubits(2)

alice.qmemory.put(Q)

# So now Alice has the two qubits in her memory:
alice.qmemory.peek(0)
alice.qmemory.peek(1)

# And Bob has:
bob.qmemory.peek(0)

# We transfer the qubit by hand, for now (next time we will make the proper connections)
alice.qmemory.pop(1)
bob.qmemory.put(Q[1])

alice.qmemory.peek(0)
alice.qmemory.peek(1)

# And Bob has:
bob.qmemory.peek(0)


#%% Entanglement swapping (without channels):

import netsquid as ns
from netsquid.components.instructions import *
from netsquid.components import QuantumMemory

Q = ns.qubits.create_qubits(4)

qmem = QuantumMemory('QM', num_positions=len(Q))
qmem.put(Q)

# Alice:
INSTR_H(qmem, positions=[0])

# Bob:
INSTR_H(qmem, positions=[2])

# print('Q[0]:\n', Q[0].qstate.qrepr.ket)
# print('Q[1]:\n', Q[1].qstate.qrepr.ket)
# print('Q[2]:\n', Q[2].qstate.qrepr.ket)
# print('Q[3]:\n', Q[3].qstate.qrepr.ket)

# Alice:
INSTR_CNOT(qmem, positions=[0, 1])
# Bob:
INSTR_CNOT(qmem, positions=[2, 3])

print('\Initial state:')
print('Q[0]:\n', Q[0].qstate.qrepr.ket)
print('Q[1]:\n', Q[1].qstate.qrepr.ket)
print('Q[2]:\n', Q[2].qstate.qrepr.ket)
print('Q[3]:\n', Q[3].qstate.qrepr.ket)



# Charlie:
INSTR_CNOT(qmem, positions=[1, 2])
INSTR_H(qmem, positions=[1])


# print('Q[0]:\n', Q[0].qstate.qrepr.ket)
# print('Q[1]:\n', Q[1].qstate.qrepr.ket)
# print('Q[2]:\n', Q[2].qstate.qrepr.ket)
# print('Q[3]:\n', Q[3].qstate.qrepr.ket)

qmem.measure(positions=[1], observable=ns.Z)
qmem.measure(positions=[2], observable=ns.Z)

# print('Q[0]:\n', Q[0].qstate.qrepr.ket)

# Bob:
INSTR_X(qmem, positions=[3])
INSTR_Z(qmem, positions=[3])

print('\nFinal state:')
print('Q[0]:\n', Q[0].qstate.qrepr.ket)
print('Q[1]:\n', Q[1].qstate.qrepr.ket)
print('Q[2]:\n', Q[2].qstate.qrepr.ket)
print('Q[3]:\n', Q[3].qstate.qrepr.ket)
