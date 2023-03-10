#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This file was made as a continuation of 'QEuropeFunctions' (Raja Yehia). It contains all the important functions for simulating a quantum network of an arbitrary number of nodes.

Netsquid has to be installed and the file 'lossmodel.py' needs to be in the same directory this file is in.

Author: Santiago Scheiner (santiagoscheiner@gmail.com)

Created: 2023-03-01

"""

import numpy as np
import scipy as sp
import netsquid as ns
from pandas import read_csv

P = read_csv('parameters.csv', header=0)
parameters = dict(zip(P['parameter'], P['value']))

parameters['f_GHZ']
##############################
# from ns.components import Channel, QuantumChannel, QuantumMemory, ClassicalChannel
# from ns.components.models.qerrormodels import FibreLossModel, DepolarNoiseModel, DephaseNoiseModel
# from ns.nodes import Node, DirectConnection
# from ns.nodes.connections import Connection
# from ns.protocols import NodeProtocol
# from ns.components.models import DelayModel
# from ns.components.models.delaymodels import FixedDelayModel, FibreDelayModel
# from ns.components import QuantumMemory
# from ns.nodes.network import Network
# from ns.qubits import ketstates as ks
# from ns.protocols.protocol import Signals
# from ns.components.qprocessor import PhysicalInstruction
# from ns.qubits import qubitapi as qapi
# from ns.components.clock import Clock
# from ns.qubits.dmtools import DenseDMRepr

##############################

f_GHZ = 8e6 #GHZ state creation attempt frequency in MHz

# time to create an n-qubit GHZ state
ghz_times = {3: np.ceil(1e9/f_GHZ),
              4: np.ceil(1e9/f_GHZ),
              5: np.ceil(1e9/f_GHZ),                 
              }

ghz_success_prob = {3: 2.5e-3,
                    4: 3.6e-3,
                    5: 9e-5,
                    }


N_nodes = 4

'''
# Prueba.
send_ghz(([Alice, Bob, Charlie], N_nodes, Qonnector))
'''
class send_ghz(ns.protocols.NodeProtocol):
    """
    Protocol performed by a Qonnector to create and send a GHZ4 state to 4 Qlients, each getting one qubit.
    It creates a processor called QonnectorGHZMemory where GHZ states are created with probability GHZ4_succ
    at a rate GHZ4_time.
    
    Parameters:
    Qlient_1, Qlient_2, Qlient_3, Qlient_4: name of the Qlients to send the qubits to (str)
    GHZ4_succ: success probability of creating a 4 qubit GHZ state
    """
    
    # def __init__(self, Qlient_1, Qlient_2, Qlient_3, Qlient_4, GHZ4_succ, node = None, name =None):
    #     super().__init__(node=node, name=name)
    #     self._GHZ_succ = GHZ4_succ
    #     self._Qlient_1 = Qlient_1
    #     self._Qlient_2 = Qlient_2
    #     self._Qlient_3 = Qlient_3
    #     self._Qlient_4 = Qlient_4

    def __init__(self, Qlients, GHZ4_succ, node = None, name =None):
        super().__init__(node=node, name=name)
        self._GHZ_succ = GHZ4_succ
        self._Qlients = Qlients
        # for n in range(N_nodes):
        #   self._Qlient_1 = Qlients[0]
        self._Qlient_1 = Qlients[0]
        self._Qlient_2 = Qlients[1]
        self._Qlient_3 = Qlients[2]
        # self._Qlient_4 = Qlients[3]
        
    def run(self):
        memories = []
        for n in range(N_nodes):
            memories.append(self.node.subcomponents["QonnectorMemoryTo{}".format(self._Qlients[n].name)])
        
        # mem1 = self.node.subcomponents["QonnectorMemoryTo{}".format(self._Qlient_1.name)]
        # mem2 = self.node.subcomponents["QonnectorMemoryTo{}".format(self._Qlient_2.name)]
        # mem3 = self.node.subcomponents["QonnectorMemoryTo{}".format(self._Qlient_3.name)]
        # mem4 = self.node.subcomponents["QonnectorMemoryTo{}".format(self._Qlient_4.name)]
        
        GHZmem = ns.components.qprocessor.QuantumProcessor("QonnectorGHZMemory", num_positions = N_nodes, fallback_to_nonphysical=True)
        self.node.add_subcomponent(GHZmem)
        
        
        GHZmatrix = np.zeros((2**N_nodes, 2**N_nodes))
        GHZmatrix[0][0]=GHZmatrix[0][-1]=GHZmatrix[-1][0]=GHZmatrix[-1][-1]=1/2
        
        GHZstate = ns.qubits.dmtools.DenseDMRepr(GHZmatrix)
        
        state_sampler = ns.qubits.state_sampler.StateSampler(qreprs=[GHZstate],
                                 probabilities=[1])
        
        qsource = ns.components.qsource.QSource("qsource1",
                          state_sampler=state_sampler,
                          num_ports=4,
                          timing_model = ns.components.models.delaymodels.FixedDelayModel(delay = ghz_times[N_nodes]),
                          status = ns.components.qsource.SourceStatus.EXTERNAL)
        clock = ns.components.clock.Clock(name="clock1",
                      start_delay=0,
                      models={"timing_model": ns.components.models.delaymodels.FixedDelayModel(delay = ghz_times[N_nodes])})
        
        
        self.node.add_subcomponent(clock)
        self.node.add_subcomponent(qsource)
        clock.ports["cout"].connect(qsource.ports["trigger"])

        for n in range(N_nodes):
            qsource.ports["qout%d"%n].connect(GHZmem.ports["qin%d"%n])
        # qsource.ports["qout0"].connect(GHZmem.ports["qin0"])
        # qsource.ports["qout1"].connect(GHZmem.ports["qin1"])
        # qsource.ports["qout2"].connect(GHZmem.ports["qin2"])
        # qsource.ports["qout3"].connect(GHZmem.ports["qin3"])
        clock.start()
        
        def route_qubits(msg):
            target = msg.meta.pop('internal', None)

            if isinstance(target, ns.components.QuantumMemory):
                if not target.has_supercomponent(self.node):
                    raise ValueError("Can't internally route to a quantummemory that is not a subcomponent.")
                target.ports['qin'].tx_input(msg)
            else:
                self.node.ports[Qonn_send].tx_output(msg)
        
        GHZmem.ports['qout'].bind_output_handler(route_qubits)
            
        
        while True:
            yield self.await_port_input(GHZmem.ports["qin0"])
            for n in range(N_nodes):
                GHZmem.pop([n], skip_noise=True, meta_data={'internal':memories[n]})
            # GHZmem.pop([1], skip_noise=True, meta_data={'internal':mem2})
            # GHZmem.pop([2], skip_noise=True, meta_data={'internal':mem3})
            # GHZmem.pop([3], skip_noise=True, meta_data={'internal':mem4})

            
            b = sp.stats.bernoulli.rvs(self._GHZ_succ)
            if b == 1:
                for n in range(N_nodes):
                    memories[n].pop([0])
                    self.node.ports["cout_{}".format(self._Qlients[n].name)].tx_output(clock.num_ticks)
                # mem2.pop([0])
                # self.node.ports["cout_{}".format(self._Qlient_2.name)].tx_output(clock.num_ticks)
                # mem3.pop([0])
                # self.node.ports["cout_{}".format(self._Qlient_3.name)].tx_output(clock.num_ticks)
                # mem4.pop([0])
                # self.node.ports["cout_{}".format(self._Qlient_4.name)].tx_output(clock.num_ticks)
            
            GHZmem.reset()
            for n in range(N_nodes):
                memories[n].reset()
            # mem2.reset()
            # mem3.reset()
            # mem4.reset()


#%%
def Sifting4(L1,L2,L3,L4):
    """Sifting Function to get a list of matching received qubit between 4 people (typically after a GHZ4 sharing)""" 
    Lres = []
    for i in range(len(L1)):
        ta, ma = L1[i]
        for j in range(len(L2)):
            tb, mb = L2[j]
            if ta == tb:
                for k in range(len(L3)):
                    tc, mc = L3[k]
                    if tb == tc:
                        for l in range(len(L4)):
                            td, md = L4[l]
                            if td == tc:
                                Lres.append((ma,mb,mc,md))  
    return Lres

#%%
'''
L1 = Qlients[0].keylist
L2 = Qlients[1].keylist
L3 = Qlients[2].keylist
L4 = Qlients[3].keylist

print(L1)
print(L2)
print(L3)
print(L4)

Lres = Sifting4(L1,L2,L3,L4)

print(Lres)
'''