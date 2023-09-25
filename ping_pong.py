import netsquid as ns
from netsquid.components import QuantumChannel

class PingPongProtocol(ns.protocols.NodeProtocol):
    def run(self):
        port = self.node.ports['qubitIO']
        while True:
            yield self.await_port_input(port)
            qubit = port.rx_input().items[0]
            observable = ns.X if self.node.name == 'Bob' else ns.Z
            outcome, _ = ns.qubits.measure(qubit, observable)
            print(f'{ns.sim_time()}: {self.node.name} measured '
                  f'{outcome} in {observable.name} basis')
            port.tx_output(qubit)
network = ns.nodes.Network(
    'PingPongNetwork', nodes=['Alice', 'Bob'])
network.add_connection('Alice', 'Bob',
    channel_to=QuantumChannel('A2B', delay=10),
    channel_from=QuantumChannel('B2A', delay=10),
    port_name_node1='qubitIO', port_name_node2='qubitIO')
proto_a = PingPongProtocol(network.nodes['Alice']).start()
proto_b = PingPongProtocol(network.nodes['Bob']).start()
qubit = ns.qubits.qubitapi.create_qubits(1)
network.nodes['Alice'].ports['qubitIO'].tx_output(qubit)
ns.sim_run(duration=50) 