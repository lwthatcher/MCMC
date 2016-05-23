class Graph:

    def __init__(self, connections, nodes):
        self.connections = connections
        self.nodes = nodes

        self.node_dict = {}
        for node in self.nodes:
            node._graph = self
            self.node_dict[node.name] = node

        self.inv_connections = {}
        for node, children in self.connections.items():
            for child in children:
                self.inv_connections[child] = self.inv_connections.setdefault(child, []) + [node]


class Node:

    def __init__(self, name, probs, graph=None, val=1, observed=False):
        self.name = name
        self._graph = graph
        self._probs = probs
        self._val = val
        self.observed = observed

    def __str__(self):
        return self.name

    def __repr__(self):
        return "(" + self.name + "=" + self.value + ")"

    @property
    def parents(self):
        p = self._graph.inv_connections.get(self.name, [])
        return [self._graph.node_dict[n] for n in p]

    @property
    def children(self):
        c = self._graph.connections.get(self.name, [])
        return [self._graph.node_dict[n] for n in c]

    @property
    def value(self):
        if self._val == 1:
            return 't'
        else:
            return 'f'

    def lookup_probability(self):
        pass
