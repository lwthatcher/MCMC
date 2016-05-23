class Graph:

    def __init__(self, connections, nodes):
        self.connections = connections
        self.nodes = nodes

        for node in self.nodes:
            node._graph = self

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

    @property
    def parents(self):
        return self._graph.inv_connections.get(self.name)

    @property
    def children(self):
        return self._graph.connections.get(self.name)

    @property
    def value(self):
        if self._val == 1:
            return 'T'
        else:
            return 'F'
