import numpy as np


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

    @property
    def hidden_nodes(self):
        result = []
        for node in self.nodes:
            if not node.observed:
                result.append(node)
        return result


class Node:

    def __init__(self, name, graph=None, val=1, observed=False):
        self.name = name
        self._graph = graph
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
        return str(self._val)


class BinaryNode(Node):

    def __init__(self, name, probs, graph=None, val=1, observed=False):
        super().__init__(name, graph=graph, val=val, observed=observed)
        self._probs = probs

    def lookup_probability(self):
        given = self._parent_values()
        prob = self._probs[given]
        if self._val == 1:
            return prob
        else:
            return 1.0 - prob

    def _parent_values(self):
        l = [p._val for p in self.parents]
        return tuple(l)

    def sample(self):
        self._val = 1
        pos = self.lookup_probability()
        for child in self.children:
            pos *= child.lookup_probability()

        self._val = 0
        neg = self.lookup_probability()
        for child in self.children:
            neg *= child.lookup_probability()

        p = pos / (pos + neg)
        out = np.random.binomial(1, p)
        self._val = out
        return out

    @property
    def value(self):
        if self._val == 1:
            return 't'
        else:
            return 'f'
