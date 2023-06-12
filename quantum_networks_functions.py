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
import pandas as pd
import os

import aux

class send_ghz(ns.protocols.NodeProtocol):
    """
    Protocol performed by a Qonnector to create and send a GHZ4 state to 4 Qlients, each getting one qubit.
    It creates a processor called QonnectorGHZMemory where GHZ states are created with probability ghz_succ
    at a rate ghz_succ.
    
    Parameters:
    Qlients: list of the Qlients to send the qubits to (str)
    GHZ_N_succ: success probability of creating a N-qubit GHZ state
    """
    
    def __init__(self, Qlients, parameters, node = None, name = None):
        super().__init__(node=node, name=name)
        self._GHZ_succ = parameters['ghz_succ']
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
                          state_sampler = state_sampler,
                          num_ports = N_nodes,
                          timing_model = ns.components.models.delaymodels.FixedDelayModel(delay = self._parameters['ghz_time']),
                          status = ns.components.qsource.SourceStatus.EXTERNAL)
        
        clock = ns.components.clock.Clock(name="clock1",
                                          start_delay = 0,
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
                # self.node.ports[Qonn_send].tx_output(msg)
                print('\n\nCHECK "ROUTE_QUBITS()" FUNCTION.')   # TODO: fix this momentary exception.
        
        GHZmem.ports['qout'].bind_output_handler(route_qubits)
            
        
        while True:
            yield self.await_port_input(GHZmem.ports["qin0"])
            for n in range(N_nodes):
                GHZmem.pop([n], skip_noise=True, meta_data={'internal':memories[n]})
            
            b = sp.stats.bernoulli.rvs(self._GHZ_succ)
            if b == 1:
                for n in range(N_nodes):
                    memories[n].pop([0])
                    self.node.ports["cout_{}".format(self._Qlients[n].name)].tx_output(clock.num_ticks)

            
            GHZmem.reset()
            for n in range(N_nodes):
                memories[n].reset()

#%%

def draw_network(G, nodes, parameters, graph_state=0):
    
    plt.close('all')
    plt.rcParams['text.usetex'] = True
    
    colours_dict = {'Qonnector': 'gray', 'Qlient': 'lightgray'}
    
    colours = []
    for node in nodes.values():
        colours.append(colours_dict[node._type])
    
    cmap = plt.cm.coolwarm
    
    edge_labels = {}
    for node in nodes.values():
        edge = (node._name, node._link)
        edge_labels[edge] = '%g km'%node._dist
    
    pos = nx.spring_layout(G)
    
    nx.draw(G, pos=pos, cmap=cmap, node_color=colours, with_labels=True, font_color='black', verticalalignment='center', horizontalalignment='center', width=1, linewidths=1, node_size=500, alpha=0.8, labels={node: node for node in G.nodes()})
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    #############################
    # SAMPLE. The edges will be given as input (variable 'graph_state' needs to be a list of edges for the graph state).
    
    edge_labels_gs = {}
    for node in nodes.values():
        edge_gs = (node._name, 'Jussieu')
        # edge_labels_gs[edge_gs] = '%g km'%node._dist # there is no distance in this case
    ##############################
    
    # Terminar esto:
    if graph_state:
        GS = nx.graph()
        for node in nodes.values():
            GS.add_edge(node._name, 'Jussieu')
        
        nx.draw_networkx_edges(GS, pos, edge_color='purple')
    
    # sm = plt.cm.ScalarMappable(norm=None, cmap=cmap)
    # plt.colorbar(sm, orientation='vertical', shrink=0.8, label=r'Distance to nearest Qonnector [km]')
    
    plt.show()
    save_dir = 'plots'
    aux.check_dir(save_dir)
    plt.savefig(save_dir + os.sep + parameters['network'] +'.png')

#%%
def sifting(nodes, Qlients):
    LISTS = pd.DataFrame()
    LISTS['time'] = None

    aggregation_functions = {'time': 'first'}

    for n in range(len(Qlients)):
        print('\rKEY: %d'%n, end='')
        col = '%s_measurement' % nodes[n].name
        LISTS[col] = None
        df = pd.DataFrame(columns=['time', col])

        for (time, measurement) in Qlients[n].keylist:
            new_line = pd.DataFrame({'time': time, col: [measurement]})
            df = pd.concat([df, new_line])
            
        LISTS = LISTS.merge(df, how='outer')

        aggregation_functions[col] = 'mean' # THIS CAN BE A PROBLEM WHEN WE ADD BIT FLIPPING. IT SHOULD KEEP THE NON-NA IN SOME WAY, NOT THE MEAN...

    LISTS = LISTS.groupby(LISTS['time']).aggregate(aggregation_functions)
    LISTS = LISTS.dropna()

    return LISTS

#%%

def ghz_prob_succ(N_nodes):
    # Gimeno Segovia 2015, eq. 4.44
    # input: amount of Qlients in the network (int)
    if N_nodes>0:
        prob = 1/(2**(N_nodes-1))
        return prob
    else:
        import sys
        print('N_nodes =', N_nodes, '\nNumber of Qlients must be an integer greater than zero.')
        sys.exit()

#%%

# TODO: delete following block
import netsquid.components.instructions as instr
from netsquid.components.qprocessor import PhysicalInstruction
from netsquid.components.qprocessor import QuantumProcessor

f_qubit_qlient = 80e6  # Qubit creation attempt frequency
Qlient_init_time = np.ceil(1e9 / f_qubit_qlient)  # time to create |0> in a Qlient node in ns

# Network parameter
fiber_coupling = 0.9  # Fiber coupling efficiency
fiber_loss = 0.18  # Loss in fiber in dB/km
fiber_dephasing_rate = 0.02  # dephasing rate in the fiber (Hz)

#%%

# Quantum operations accessible to the Qonnectors
qonnector_physical_instructions = [
    PhysicalInstruction(instr.INSTR_INIT, duration = Qlient_init_time),
    PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_X, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_Z, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_S, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_I, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_CNOT, duration=4, parallel=True),
    PhysicalInstruction(instr.INSTR_MEASURE, duration=1, parallel=True, topology=[0, 1]),
    PhysicalInstruction(instr.INSTR_MEASURE_BELL, duration=1, parallel=True),
    PhysicalInstruction(instr.INSTR_SWAP, duration=1, parallel=True)
]

# Quantum operations accessible to the Qlient
qlient_physical_instructions = [
    PhysicalInstruction(instr.INSTR_INIT, duration = Qlient_init_time),
    PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_X, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_Z, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_S, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_I, duration=1, parallel=True, topology=[0]),
    PhysicalInstruction(instr.INSTR_MEASURE, duration=1, parallel=False, topology=[0])
]


class Qlient_node(ns.nodes.Node):
    """A Qlient node
    
    Parameters:
    name: name of the Qlient
    phys_instruction: list of physical instructions for the Qlient
    keylist: list of bits for QKD
    ports: list of two ports: one to send to Qonnector and one to receive
    """

    def __init__(self, name, phys_instruction, keylist=None, listports=None):
        super().__init__(name=name)
        qmem = ns.components.qprocessor.QuantumProcessor("QlientMemory{}".format(name), num_positions=1,
                                phys_instructions=phys_instruction)
        self.qmemory = qmem
        self.keylist = keylist
        self.listports = listports


class Qonnector_node(ns.nodes.Node):
    """A Qonnector node
    
    Parameters:
    QlientList: List of connected Qlients
    QlientPorts: Dictionnary of the form {Qlient: [port_to_send, port_to_receive]}
    QlientKeys : Dictionnary for QKD of the form {Qlient: [key]}
    """

    def __init__(self, name, QlientList=None,
                 QlientPorts=None, QlientKeys=None):
        super().__init__(name=name)
        self.QlientList = QlientList
        self.QlientPorts = QlientPorts
        self.QlientKeys = QlientKeys

class QEurope():

    def __init__(self, name):
        """ Initialisation of a Quantum network

        Parameter:
        name: name of the network (str) /!\ Expected name should start with 'Qonnector' /!\
        """
        self.network = ns.nodes.network.Network(name)
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

        qchannel1 = ns.components.QuantumChannel("QuantumChannelSto{}".format(qlientname), length=distance, delay=1, models={"quantum_loss_model": ns.components.models.qerrormodels.FibreLossModel(p_loss_init=1 - fiber_coupling, p_loss_length=fiber_loss), "quantum_noise_model": ns.components.models.qerrormodels.DephaseNoiseModel(dephase_rate=fiber_dephasing_rate, time_independent=True)})
        
        qchannel2 = ns.components.QuantumChannel("QuantumChannel{}toS".format(qlientname),
                                                 length=distance,
                                                 delay=1,
                                                 models={"quantum_loss_model": ns.components.models.qerrormodels.FibreLossModel(p_loss_init=1 - fiber_coupling, p_loss_length=fiber_loss), "quantum_noise_model": ns.components.models.qerrormodels.DephaseNoiseModel(dephase_rate = fiber_dephasing_rate, time_independent=True)})

        Qonn_send, Qlient_receive = network.add_connection(qonnectorto, qlientname, channel_to=qchannel1, label="quantumS{}".format(qlientname))
        Qlient_send, Qonn_receive = network.add_connection(qlientname, qonnectorto, channel_to=qchannel2, label="quantum{}S".format(qlientname))

        # Update the Qonnector's properties
        qmem = QuantumProcessor("QonnectorMemoryTo{}".format(qlientname), num_positions=2,
                                phys_instructions=qonnector_physical_instructions)
        Qonnector.add_subcomponent(qmem)
        Qonnector.QlientList.append(qlientname)
        Qonnector.QlientPorts[qlientname] = [Qonn_send, Qonn_receive]
        Qonnector.QlientKeys[qlientname] = []

        # Update Qlient ports
        Qlient.listports = [Qlient_send, Qlient_receive]
