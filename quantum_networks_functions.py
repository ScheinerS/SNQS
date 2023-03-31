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

import pandas as pd

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
                          num_ports=N_nodes,
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
def sifting(nodes, Qlients):
    LISTS = pd.DataFrame()
    LISTS['time'] = None

    aggregation_functions = {'time': 'first'}

    for n in range(len(Qlients)):
        print('KEY: ', n)
        col = '%s_measurement' % nodes[n].name
        LISTS[col] = None
        df = pd.DataFrame(columns=['time', col])

        for (time, measurement) in Qlients[n].keylist:
            new_line = pd.DataFrame({'time': time, col: [measurement]})
            df = pd.concat([df, new_line])

        LISTS = LISTS.merge(df, how='outer')

        aggregation_functions[col] = 'mean' # THIS CAN BE A PROBLEM WHEN WE ADD BIT FLIPPING. IT SHOULD KEEP THE NON-NA IN SOME WAY, NO THE MEAN...

    LISTS = LISTS.groupby(LISTS['time']).aggregate(aggregation_functions)
    LISTS = LISTS.dropna()

    return LISTS


class QEurope():

    def __init__(self, name):
        """ Initialisation of a Quantum network

        Parameter:
        name: name of the network (str) /!\ Expected name should start with 'Qonnector' /!\
        """
        self.network = Network(name)
        self.name = name

    def Add_Qonnector(self, qonnectorname):
        """Method to add a Qonnector to the network

        Parameter :
        qonnectorname: name tof the Qonnector to add (str)
        """

        Qonnector = Qonnector_node(qonnectorname, QlientList=[], QlientPorts={}, QlientKeys={})
        self.network.add_node(Qonnector)

    def Add_Qlient(self, qlientname, distance, qonnectorto):

        """ Method to add a Qlient to the network. It creates a Quantum Processor at the Qonnector qonnectorto
         that is linked to the new Qlient through a fiber.

        Parameters :
        qlientname: name of the qlient to add (str)
        distance: distance from the Qonnector to the new node in km
        qonnectorto: Name of the Qonnector to attach the Qlient to (str)
        """

        network = self.network
        # Check that the Qonnector has space for the new qlient
        Qonnector = network.get_node(qonnectorto)
        if len(Qonnector.QlientList) == 'Max_Qlient':
            raise ValueError("You have reached the maximum Qlient capacity for this Qonnector.")

        # creates a qlient and adds it to the network
        Qlient = Qlient_node(qlientname, qlient_physical_instructions, keylist=[], listports=[])
        network.add_node(Qlient)

        # Create quantum channels and add them to the network

        qchannel1 = QuantumChannel("QuantumChannelSto{}".format(qlientname), length=distance, delay=1,
                                   models={"quantum_loss_model": FibreLossModel(p_loss_init=1 - fiber_coupling,
                                                                                p_loss_length=fiber_loss),
                                           "quantum_noise_model": DephaseNoiseModel(dephase_rate=fiber_dephasing_rate,
                                                                                    time_independent=True)})
        qchannel2 = QuantumChannel("QuantumChannel{}toS".format(qlientname), length=distance, delay=1,
                                   models={"quantum_loss_model": FibreLossModel(p_loss_init=1 - fiber_coupling,
                                                                                p_loss_length=fiber_loss),
                                           "quantum_noise_model": DephaseNoiseModel(dephase_rate=fiber_dephasing_rate,
                                                                                    time_independent=True)})

        Qonn_send, Qlient_receive = network.add_connection(
            qonnectorto, qlientname, channel_to=qchannel1, label="quantumS{}".format(qlientname))
        Qlient_send, Qonn_receive = network.add_connection(
            qlientname, qonnectorto, channel_to=qchannel2, label="quantum{}S".format(qlientname))

        # Update the Qonnector's properties
        qmem = QuantumProcessor("QonnectorMemoryTo{}".format(qlientname), num_positions=2,
                                phys_instructions=qonnector_physical_instructions)
        Qonnector.add_subcomponent(qmem)
        Qonnector.QlientList.append(qlientname)
        Qonnector.QlientPorts[qlientname] = [Qonn_send, Qonn_receive]
        Qonnector.QlientKeys[qlientname] = []

        # Update Qlient ports
        Qlient.listports = [Qlient_send, Qlient_receive]
'''
        def route_qubits(msg):
            target = msg.meta.pop('internal', None)

            if isinstance(target, QuantumMemory):
                if not target.has_supercomponent(Qonnector):
                    raise ValueError("Can't internally route to a quantummemory that is not a subcomponent.")
                target.ports['qin'].tx_input(msg)
            else:
                Qonnector.ports[Qonn_send].tx_output(msg)

        # Connect the Qonnector's ports
        qmem.ports['qout'].bind_output_handler(route_qubits)  # port to send to Qlient
        Qonnector.ports[Qonn_receive].forward_input(qmem.ports["qin"])  # port to receive from Qlient

        # Connect the Qlient's ports 
        Qlient.ports[Qlient_receive].forward_input(Qlient.qmemory.ports["qin"])  # port to receive from qonnector
        Qlient.qmemory.ports["qout"].forward_output(Qlient.ports[Qlient_send])  # port to send to qonnector

        # Classical channels on top of that
        cchannel1 = ClassicalChannel("ClassicalChannelSto{}".format(qlientname), length=distance, delay=1)
        cchannel2 = ClassicalChannel("ClassicalChannel{}toS".format(qlientname), length=distance, delay=1)

        network.add_connection(qonnectorto, qlientname, channel_to=cchannel1,
                               label="ClassicalS{}".format(qlientname), port_name_node1="cout_{}".format(qlientname),
                               port_name_node2="cin")
        network.add_connection(qlientname, qonnectorto, channel_to=cchannel2,
                               label="Classical{}S".format(qlientname), port_name_node1="cout",
                               port_name_node2="cin_{}".format(qlientname))
'''