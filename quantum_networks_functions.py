#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This file was made as a continuation of 'QEuropeFunctions' (Raja Yehia). It contains all the important functions for simulating a quantum network of an arbitrary number of nodes.

Netsquid has to be installed and the file 'lossmodel.py' needs to be in the same directory this file is in.

Author: Santiago Scheiner (santiagoscheiner@gmail.com)

Created: 2023-03-01

"""

import numpy as np

import netsquid as ns

# import netsquid.components.instructions as instr
# import netsquid.components.qprogram as qprog
# import random 
# from scipy.stats import bernoulli
# import logging
# import math
# import numpy as np

# from netsquid.components import Channel, QuantumChannel, QuantumMemory, ClassicalChannel
# from netsquid.components.models.qerrormodels import FibreLossModel, DepolarNoiseModel, DephaseNoiseModel
# from netsquid.nodes import Node, DirectConnection
# from netsquid.nodes.connections import Connection
from netsquid.protocols import NodeProtocol
# from netsquid.components.models import DelayModel
from netsquid.components.models.delaymodels import FixedDelayModel, FibreDelayModel
from netsquid.components import QuantumMemory
from netsquid.qubits.state_sampler import StateSampler
from netsquid.components.qsource import QSource, SourceStatus
from netsquid.components.qprocessor import QuantumProcessor
# from netsquid.nodes.network import Network
# from netsquid.qubits import ketstates as ks
# from netsquid.protocols.protocol import Signals
# from netsquid.components.qprocessor import PhysicalInstruction
# from netsquid.qubits import qubitapi as qapi
from netsquid.components.clock import Clock
from netsquid.qubits.dmtools import DenseDMRepr

N_nodes = 3 # DELETE AFTERWARDS.

f_GHZ = 8e6 #GHZ state creation attempt frequency in MHz

# time to create an n-qubit GHZ state
ghz_times = {3: np.ceil(1e9/f_GHZ),
             4: np.ceil(1e9/f_GHZ),
             5: np.ceil(1e9/f_GHZ),                 
             }

ghz_success_prob = { 3: 2.5e-3,
                     4: 3.6e-3,
                     5: 9e-5,
                     }


class SendGHZ(NodeProtocol):
    """Protocol performed by a Qonnector to create and send a GHZ state to N_nodes Qlients, each getting one qubit.
     It creates a processor called QonnectorGHZMemory where GHZ states are created with probability GHZ_succ
     at a rate GHZ3_time.
     
     Parameters:
     Qlient_1, Qlient_2, Qlient_3: name of the Qlients to send the qubits to (str)
     GHZ3_succ: success probability of creating a 3 qubit GHZ state
     """
     
    
    def __init__(self, Qlient_1, Qlient_2, Qlient_3, N_nodes, node = None, name =None):
        super().__init__(node=node, name=name)
        self._GHZ_succ = ghz_success_prob[N_nodes]
        self._Qlient_1 = Qlient_1
        self._Qlient_2 = Qlient_2
        self._Qlient_3 = Qlient_3
        
    def run(self):
        mem1 = self.node.subcomponents["QonnectorMemoryTo{}".format(self._Qlient_1.name)]
        mem2 = self.node.subcomponents["QonnectorMemoryTo{}".format(self._Qlient_2.name)]
        mem3 = self.node.subcomponents["QonnectorMemoryTo{}".format(self._Qlient_3.name)]
        
        GHZmem = QuantumProcessor("QonnectorGHZMemory", num_positions=N_nodes,
                                fallback_to_nonphysical=True)
        self.node.add_subcomponent(GHZmem)
                
        GHZmatrix = np.zeros((2**N_nodes, 2**N_nodes))
        GHZmatrix[0][0]=GHZmatrix[0][-1]=GHZmatrix[-1][0]=GHZmatrix[-1][-1]=1/2
        
        
        GHZstate = DenseDMRepr(GHZmatrix)
        
        state_sampler = StateSampler(qreprs=[GHZstate],
                                 probabilities=[1])
        
        qsource = QSource("qsource1",
                          state_sampler=state_sampler,
                          num_ports=3,
                          timing_model=FixedDelayModel(delay=ghz_times[N_nodes]),
                          status=SourceStatus.EXTERNAL)
        clock = Clock(name="clock1",
                      start_delay=0,
                      models={"timing_model": FixedDelayModel(delay=ghz_times[N_nodes])})
        
        
        self.node.add_subcomponent(clock)
        self.node.add_subcomponent(qsource)
        clock.ports["cout"].connect(qsource.ports["trigger"])

        
        qsource.ports["qout0"].connect(GHZmem.ports["qin0"])
        qsource.ports["qout1"].connect(GHZmem.ports["qin1"])
        qsource.ports["qout2"].connect(GHZmem.ports["qin2"])
        clock.start()
        
        def route_qubits(msg):
            target = msg.meta.pop('internal', None)

            if isinstance(target, QuantumMemory):
                if not target.has_supercomponent(self.node):
                    raise ValueError("Can't internally route to a quantummemory that is not a subcomponent.")
                target.ports['qin'].tx_input(msg)
            else:
                self.node.ports[Qonn_send].tx_output(msg)
        
        GHZmem.ports['qout'].bind_output_handler(route_qubits)
            
        
        while True:
            yield self.await_port_input(GHZmem.ports["qin0"])
            
            GHZmem.pop([0], skip_noise=True, meta_data={'internal':mem1})
            GHZmem.pop([1], skip_noise=True, meta_data={'internal':mem2})
            GHZmem.pop([2], skip_noise=True, meta_data={'internal':mem3})

            #print(mem1.peek([0]))
            
            b = bernoulli.rvs(self._GHZ_succ)
            if b == 1:
                mem1.pop([0])
                self.node.ports["cout_{}".format(self._Qlient_1.name)].tx_output(clock.num_ticks)
                mem2.pop([0])
                self.node.ports["cout_{}".format(self._Qlient_2.name)].tx_output(clock.num_ticks)
                mem3.pop([0])
                self.node.ports["cout_{}".format(self._Qlient_3.name)].tx_output(clock.num_ticks)
                
            GHZmem.reset()
            mem1.reset()
            mem2.reset()
            mem3.reset()
