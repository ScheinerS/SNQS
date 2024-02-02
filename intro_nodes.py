#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 18:46:28 2023

@author: santiago
"""

#%% Exercise 111

import netsquid as ns
from netsquid.components import QuantumMemory
import netsquid.components.instructions as ins

Q = ns.qubits.create_qubits(3)

qmem = QuantumMemory('QM', num_positions=len(Q))
qmem.put(Q)

ins.INSTR_X(qmem, positions=[0])
ins.INSTR_X(qmem, positions=[1])
ins.INSTR_X(qmem, positions=[2])

print('Q[0]:\n', Q[0].qstate.qrepr.ket)
print('Q[1]:\n', Q[1].qstate.qrepr.ket)
print('Q[2]:\n', Q[2].qstate.qrepr.ket)


#%% Exercise GHZ

Q = ns.qubits.create_qubits(4)

qmem = QuantumMemory('QM', num_positions=len(Q))
qmem.put(Q)

ins.INSTR_H(qmem, positions=[0])
ins.INSTR_CNOT(qmem, positions=[0, 1])
ins.INSTR_CNOT(qmem, positions=[1, 2])
ins.INSTR_CNOT(qmem, positions=[2, 3])

print('Q[0]:\n', Q[0].qstate.qrepr.ket)

print('X measurements:')
[qmem.measure(positions=[i], observable=ns.X) for i in range(len(Q))]

print('Q[0]:\n', Q[0].qstate.qrepr.ket)

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

# Nodes:
    
from netsquid.nodes import Node
alice = Node("Alice")
bob = Node("Bob")
print(alice)
print(bob)

# Classical Channels:
import netsquid as ns

from netsquid.components import Channel, QuantumChannel
channel = Channel(name="ch_A_to_B")
channel

# Sending a message:
channel.send("Hello.")
ns.sim_run()

# Receiving the message:
items, delay = channel.receive()
items
delay

# Adding delays to the messages:

Channel(name="DelayChannel", delay=10)


#%%

# Defining a Q channel:
Qchannel = QuantumChannel(name="QC_Alice_to_Bob")
Qchannel


Q = ns.qubits.create_qubits(1)

Qchannel.send(Q[0])
ns.sim_run()

items, delay = Qchannel.receive()
items
delay

# ns.sim_reset()

#%%

# Adding properties to the channel

from netsquid.components.models.qerrormodels import FibreLossModel

from netsquid.components.qchannel import QuantumChannel

loss_model = FibreLossModel(p_loss_init=0.83, p_loss_length=0.2)


from netsquid.components.models.qerrormodels import QuantumErrorModel

error_model = QuantumErrorModel
qchannel = QuantumChannel("MyQChannel", length=20, models={'quantum_loss_model': loss_model})

# TODO: terminar esto y agregarlo en algun lado.













from netsquid.components import QuantumMemory


#%%
# Creating a Quantum channel to be connected to the memory:

Qchannel = QuantumChannel(name="QC")

# We create a qubit to send:
Q = ns.qubits.create_qubits(1)
Q[0]


# Connecting a Qchannel to a memory.

qmem = QuantumMemory("QM", num_positions=1)
qmem.peek(0)
# it's empty.

# We connect the receive port of the channel to the input port of the memory:
Qchannel.ports['recv'].connect(qmem.ports['qin'])

Q = ns.qubits.create_qubits(1)

Qchannel.send(Q[0])
ns.sim_run()

items, delay = Qchannel.receive()
items
delay

# The qubit should now be in the memory:
qmem.peek(0)


#%%
# Again, but the other way around:

# We create a new channel
Qchannel = QuantumChannel(name="QC_2")


qmem = QuantumMemory("QM_2", num_positions=1)
qmem.peek(0)
# it's empty.

# Now, we connect the sending port of the channel to the output port of the memory:
Qchannel.ports['send'].connect(qmem.ports['qout'])

# We create a qubit to send:
Q = ns.qubits.create_qubits(1)
Q[0]

# We put the qubit in the memory:
qmem.put(Q)
qmem.peek(0)

# We pop the qubit from the memory:
qmem.pop(0)
qmem.peek(0)
# And we see the memory is now empty.

# And on the other end of the channel, we receive:
items, delay = Qchannel.receive()
items
delay
# And again, it's the qubit we sent.

#%% Ports

import netsquid as ns
from netsquid.components import QuantumMemory
# Test:

# qmem_A.reset()
# qmem_B.reset()

# We define 
qmem_A = QuantumMemory("QMA", num_positions=2)
qmem_B = QuantumMemory("QMB", num_positions=2)

qmem_A.peek([0,1])
qmem_B.peek([0,1])

# Both memories are empty.

# We create two qubits and we put them in qmem_A:
Q = ns.qubits.create_qubits(2)
qmem_A.put(Q)

qmem_A.peek([0,1])
qmem_B.peek([0,1])


# We connect the channel to the memories:

qmem_A.ports['qout0'].connect(Qchannel.ports['send'])

Qchannel.ports['recv'].connect(qmem_B.ports['qin0'])

Qchannel.send(Q[0])
ns.sim_run()

items, delay = Qchannel.receive()
items
delay
# qmem_A.pop(0)
# ns.sim_run()


qmem_A.peek([0,1])
qmem_B.peek([0,1])

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
