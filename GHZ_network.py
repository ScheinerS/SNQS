#!/usr/bin/env python

import netsquid as ns
import pandas as pd
import os

import QEuropeFunctions as qe
import aux
import networkx as nx
import quantum_networks_functions as qnf
import plot_network as pn
import local_complementation as lc

# %%
# class Network():
#     def __init__(self, node_name, qonnector, dist_to_Qonnector, node_type):
        
class Node:
    def __init__(self, node_name, links, dist_to_Qonnector, node_type, number_of_qubits=1):
        self._name = node_name
        self._links = links # List of neighbours.
        self._dist = dist_to_Qonnector
        self._type = node_type # Qonnector, Qlient.
        self._keylist = []   # shared one-time pad
        self._number_of_qubits = number_of_qubits   # number of qubits for this node
        self._qubits = ns.qubits.create_qubits(number_of_qubits)

def combine_nodes_qubits(nodes, verbose=False):
    N_Qubits = 0
    for node in nodes.values():
        if verbose:
            print('Node:\t%s\t%s'%(node._name, node._number_of_qubits))
        N_Qubits += node._number_of_qubits
        
    Q = ns.qubits.create_qubits(N_Qubits)
    for q in Q[1:]:
        Q[0].combine(q)
    
    if verbose:
        print('\nQ = ')
        qnf.print_state_as_ket(Q, 'plain', verbose=1)
    
    return Q


def initialise_qubits(nodes, verbose=False):
    # receives the dictionary of nodes in the state |0> and returns it in the |+> state.
    for node in nodes.values():
        Q = combine_nodes_qubits(nodes, verbose=verbose)
        state = qnf.print_state_as_ket(Q, print_format='plain', verbose=verbose)
        
        qmem = ns.components.qmemory.QuantumMemory('MyQMem', num_positions=len(Q))
        qmem.put(Q)
        
        for i in range(len(Q)):
            print('H on Q[%d]'%i)
            ns.components.instructions.INSTR_H(qmem, positions=[i])
            state = qnf.print_state_as_ket(Q, print_format='plain', verbose=verbose)
    
    return Q, state


#%%

parameters = aux.read_parameters('parameters')
parameters['network'] = 'star_02' #'QEurope' # TODO: fix this. If the network name is on the same column as the values, they all get converted to 'str'...

network = pd.read_csv('networks' + os.sep + parameters['network'] + '.csv', header=0)

flags = {'draw_network': 1,
         'print_parameters': 0,
         'save_parameters': 0,
         'print_lists': 1,
         'save_results': 0,
         'runtimes': 0,
         }

if flags['print_parameters']:
    print('\n', parameters, '\n')

if flags['save_parameters']:
    directory = 'previous_parameters'
    aux.check_dir(directory)
    aux.save_parameters(directory)

if flags['runtimes']:
    import time
    start = time.time()

nodes = {}

for n in range(len(network)):
    nodes[network['Name'].at[n]] = Node(network['Name'].at[n], network['Link'].at[n], network['Distance to Qonnector (km)'].at[n], network['Type'].at[n])




def qonnect_star_networks(nodes, verbose=1):
    
    # Star network verification:
    Qonnectors = []
    Qlients = []
    
    for node in nodes.values():
        if node._type=='Qonnector':
            Qonnectors.append(node)
            
        elif node._type=='Qlient':
            Qlients.append(node)
    
    if verbose:
        print('\nQonnectors:')
        for q in Qonnectors:
            print('\t', q._name)
        print('\nQlients:')
        for q in Qlients:
            print('\t', q._name)
    
    Q = []
    for node in nodes.values():
        for qubit in node._qubits:
            Q.append(qubit)

    lc.combine_Q(Q, verbose=0)
    
    qmem = ns.components.qmemory.QuantumMemory('MyQMem', num_positions=len(Q))
    qmem.put(Q)
    
    step = 0
    Graph_States = {}
    Ket = {}
    
    if verbose:
        print('STEP %d - Initial state:'%step)
    
    state = qnf.print_state_as_ket(Q, verbose=verbose)  
    
    S = nx.Graph()
    Graph_States[step] = S
    Ket[step] = state
    
    # Step 1:
    step += 1
    
    for node in nodes.values():
        if node._type=='Qonnector':
            ns.components.instructions.INSTR_H(qmem, positions=[0])
    
    if verbose:
        print("STEP %d - H on Qonnector's qubit:"%step)
        qnf.print_state_as_ket(Q)
    
    S = nx.Graph()
    Graph_States[step] = S
    
    ###########
    # CX gates:
    step += 1
        
    if verbose:
        print("STEP %d - H on Qonnector's qubit:"%step)
        qnf.print_state_as_ket(Q)
        
    for node in Qlients:
        
        ns.components.instructions.INSTR_H(qmem, positions=[0])
    
    '''
    print('STEP 0:\tH on Q[0]')
    ns.components.instructions.INSTR_H(qmem, positions=[0])
    lc.print_state_as_ket(Q)
    
    print('STEP 1:\tQonnector applies CX on Q[0] and Q[1]')
    ns.components.instructions.INSTR_CX(qmem, positions=[0,1])
    lc.print_state_as_ket(Q)
    
    print('STEP 2:\tQonnector applies CX on Q[0] and Q[2]')
    ns.components.instructions.INSTR_CX(qmem, positions=[0,2])
    lc.print_state_as_ket(Q)
    '''
    
    return Q, Graph_States
    '''
    Graph_States = []
    for step in range(len(nodes)):
        S = nx.Graph()
        S_edges = pn.state_to_graph_state(nodes, state=1) # TODO: state should later be the state, not a '1'.
        S_edges = S_edges[:i] # TODO: This line should be removed once state_to_graph_state() is actually working.
        S.add_edges_from(S_edges)
        Graph_States.append(S)
    '''
    
qonnect_star_networks(nodes)


#%%

def verification(Q):
    flag = False
    
    '''
    XXX...XY
    XXX...YX
    
    YXX...X
    '''
    return flag



ns.sim_reset()

# Creation of a network instance
net2 = qnf.QEurope("net")

# Initialisation of the nodes
net = net2.network

# Qonnector
Qonnectors = {}
Qlients = {}

for node in nodes.values():
    if node._type == 'Qonnector':
        net2.Add_Qonnector(node._name)
        # Qonnectors.append(net.get_node(node._name))
        Qonnectors[node._name] = net.get_node(node._name)
    elif node._type == 'Qlient':
        net2.Add_Qlient(node._name, node._dist, node._links)
        # Qlients.append(net.get_node(node._name))
        Qlients[node._name] = net.get_node(node._name)
    else:
        print('Unknown node type: "%s" for node "%s". Nodes must be either of type "Qonnector" or "Qlient".'%(node._type, node._name))
        
if flags['draw_network']:
    N = nx.Graph()

    edges = list(zip(network['Name'], network['Link']))

    N.add_edges_from(edges)
    
    Graph_States = []
    Kets = []
    
    # for i in range(len(nodes)):
    #     S = nx.Graph()
    #     S_edges = pn.state_to_graph_state(nodes, state=1) # TODO: state should later be the state, not a '1'.
    #     S_edges = S_edges[:i] # TODO: This line should be removed once state_to_graph_state() is actually working.
    #     S.add_edges_from(S_edges)
    #     Graph_States.append(S)

    N_pos = nx.spring_layout(N)
    
    for step in range(len(Graph_States)):
        # state = lc.print_state_as_ket()
        # Kets.append()
        pn.draw_network(N, nodes, N_pos, parameters, S=Graph_States[step], plot_graph_state=True, step=step, ket=True)

# %%

for q in Qonnectors:
    ghzprotocol = qnf.send_ghz(Qlients, parameters, q)  # THIS LINE IS WRONG. THE GHZ STATE SHOULD BE DISTRIBUTED ONLY TO THE NODES LINKED TO THE QONNECTOR q, NOT TO ALL QLIENTS.
    print('Check this line.')

ghzprotocol.start()

protocols = []
for node in nodes.values():
    # ESTO NO FUNCIONA:
    #protocols.append(qe.ReceiveProtocol(Qonnectors.values(), qe.Qlient_meas_succ, qe.Qlient_meas_flip, False, Qlients[node._name]))
    # protocols[node._name].start()
    print('FIX THIS LATER...')
    
# Simulation starting
stat = ns.sim_run(duration=parameters['simtime'])

# Adding dark count for each Qlient
for node in nodes:
    qe.addDarkCounts(Qlients[node.name].keylist, parameters['DCRateWorst'] * parameters['DetectGateWorst'],
                     int(parameters['simtime'] / parameters['ghz_time']))

#%% Sifting.

LISTS = qnf.sifting(nodes, Qlients) # Sifting to keep the qubit from the same GHZ state


if flags['print_lists']:
    print("\nNumber of qubits received by the %d Qlients: %d" % (len(nodes), len(LISTS)))

    print(LISTS)
    # print("QBER:\t%g" % qe.estimQBERGHZ4(Lres))

if flags['save_results']:
    print('TODO: save_results')

if flags['runtimes']:
    end = time.time()
    print('Elapsed time:\t%d\tseconds'%(end-start))

#%%

# if __name__=='__main__':
#     print()