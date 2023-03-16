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
import matplotlib.pyplot as plt
import networkx as nx

# P = read_csv('parameters.csv', header=0)
# parameters = dict(zip(P['parameter'], P['value']))

# parameters['f_GHZ']

# f_GHZ = 8e6 #GHZ state creation attempt frequency in MHz

# # time to create an n-qubit GHZ state
# ghz_times = {3: np.ceil(1e9/f_GHZ),
#               4: np.ceil(1e9/f_GHZ),
#               5: np.ceil(1e9/f_GHZ),                 
#               }

# ghz_success_prob = {3: 2.5e-3,
#                     4: 3.6e-3,
#                     5: 9e-5,
#                     }


# N_nodes = 4

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
    Qlients: list of the Qlients to send the qubits to (str)
    GHZ_N_succ: success probability of creating a N-qubit GHZ state
    """
    

    def __init__(self, Qlients, parameters, node = None, name = None):
        super().__init__(node=node, name=name)
        self._GHZ_succ = parameters['GHZ4_succ']
        self._Qlients = Qlients
        self._parameters = parameters
        
        
    def run(self):
        
        N_nodes = len(self._Qlients)
        memories = []
        for n in range(N_nodes):
            memories.append(self.node.subcomponents["QonnectorMemoryTo{}".format(self._Qlients[n].name)])
        
        GHZmem = ns.components.qprocessor.QuantumProcessor("QonnectorGHZMemory", num_positions = N_nodes, fallback_to_nonphysical=True)
        self.node.add_subcomponent(GHZmem)
        
        
        GHZmatrix = np.zeros((2**N_nodes, 2**N_nodes))
        GHZmatrix[0][0]=GHZmatrix[0][-1]=GHZmatrix[-1][0]=GHZmatrix[-1][-1]=1/2
        
        GHZstate = ns.qubits.dmtools.DenseDMRepr(GHZmatrix)
        
        state_sampler = ns.qubits.state_sampler.StateSampler(qreprs=[GHZstate], probabilities=[1])
        
        qsource = ns.components.qsource.QSource("qsource1",
                          state_sampler=state_sampler,
                          num_ports=4,
                          timing_model = ns.components.models.delaymodels.FixedDelayModel(delay = self._parameters['ghz_time']), # ghz_times[N_nodes]
                          status = ns.components.qsource.SourceStatus.EXTERNAL)
        clock = ns.components.clock.Clock(name="clock1",
                      start_delay=0,
                      models={"timing_model": ns.components.models.delaymodels.FixedDelayModel(delay = self._parameters['ghz_time'])})
        
        
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

def draw_network(G, nodes):
    plt.close('all')
    
    colours = []
    for k in nodes.keys():
        colours.append(nodes[k].dist) # Value map for the colouring of the nodes.
    
    cmap = plt.cm.coolwarm
    
    node_positions = {} # pos (dict or None optional (default=None)) – Initial positions for nodes as a dictionary with node as keys and values as a coordinate list or tuple. If None, then use random initial positions.
    for k in nodes.keys():
        node_positions[k] = (np.sqrt(nodes[k].dist), np.sqrt(nodes[k].dist))
    
    nx.draw(G, cmap=cmap, node_color=colours, with_labels=True, font_color='black', verticalalignment='center', horizontalalignment='center')
    
    
    sm = plt.cm.ScalarMappable(cmap=cmap)#, norm=plt.Normalize(vmin = vmin, vmax=vmax))
    sm._A = []
    plt.colorbar(sm, orientation='vertical', shrink=0.8, label=r'Distance to Qonnector')
    
    
    plt.show()

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
import pandas as pd

def Sifting(LISTS):
    
    """Sifting Function to get a list of matching received qubit between 4 people (typically after a GHZ4 sharing)""" 
    Lres = []
    '''
    LISTS = [L1, L2, L3, L4]
    '''

    for (time, measurement) in LISTS[0]:
        print(time)
        print(measurement)
        is_in_all_lists = True # It is in all other lists so far.
        for i in range(1,len(LISTS)):
            # print(LISTS[i])
            if time in LISTS[i]:
                print()
                #### TERMINAR.

    # for i in range(len(L1)):
    #     time_a, measurement_a = L1[i]
    #     for j in range(len(L2)):
    #         tb, mb = L2[j]
    #         if ta == tb:
    #             for k in range(len(L3)):
    #                 tc, mc = L3[k]
    #                 if tb == tc:
    #                     for l in range(len(L4)):
    #                         td, md = L4[l]
    #                         if td == tc:
    #                             Lres.append((ma,mb,mc,md))  
    # return Lres

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