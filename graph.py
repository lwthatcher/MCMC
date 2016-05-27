import numpy as np
import math
from scipy.stats import norm

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

    def lookup_probability(self):
        return 0

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

    def __init__(self, name, probs, **kwargs):
        super().__init__(name, **kwargs)
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


class MetropolisNode(Node):

    def __init__(self, name, cand_dist=None, **kwargs):
        super().__init__(name, **kwargs)
        if cand_dist is None:
            cand_dist = [0, 1]
        self.cd_params = cand_dist

    def get_candidate_value(self):
        mu = self.cd_params[0]
        sigma = math.sqrt(self.cd_params[1])
        return np.random.normal(mu, sigma)

    def sample(self):
        cand = self.get_candidate_value()
        last = self._val

        fxt = self.lookup_probability()
        for child in self.children:
            fxt += child.lookup_probability()

        self._val = cand
        fxs = self.lookup_probability()
        for child in self.children:
            fxs += child.lookup_probability()

        u = np.random.uniform()
        if u < fxs - fxt:
            self._val = cand
        else:
            self._val = last


class NormalNode(MetropolisNode):
    def __init__(self, name, mean, var, **kwargs):
        super().__init__(name, **kwargs)
        self.mean = mean
        self.var = var

    @property
    def stdev(self):
        return math.sqrt(self.var)

    def lookup_probability(self):
        return norm.logpdf(self.value, loc=self.mean, scale=self.stdev)
