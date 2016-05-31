import numpy as np
import numbers
import math
from scipy.stats import norm
from scipy.special import gammaln


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

    def __init__(self, name, cand_var=None, **kwargs):
        super().__init__(name, **kwargs)
        if cand_var is None:
            cand_var = 1.
        self.cd_var = cand_var

    def get_candidate_value(self):
        mu = self._val
        sigma = math.sqrt(self.cd_var)
        return np.random.normal(mu, sigma)

    def sample(self, cand=None):
        if cand is None:
            cand = self.get_candidate_value()
        last = self._val

        fxt = self.lookup_probability()
        for child in self.children:
            fxt += child.lookup_probability()

        self._val = cand
        fxs = self.lookup_probability()
        for child in self.children:
            fxs += child.lookup_probability()

        u = np.log(np.random.uniform())
        if u < fxs - fxt:
            self._val = cand
        else:
            self._val = last

        return self._val

    def parameter(self, param):
        if isinstance(param, Node):
            return param._val
        elif isinstance(param, str):
            return self._graph.node_dict[param]._val
        else:
            return param


class NormalNode(MetropolisNode):
    def __init__(self, name, mean, var, **kwargs):
        super().__init__(name, **kwargs)
        self._mean = mean
        self._var = var

    @property
    def mean(self):
        return self.parameter(self._mean)

    @property
    def var(self):
        return self.parameter(self._var)

    def lookup_probability(self):
        x = self._val
        return -1/2 * (np.log(self.var) + 1/self.var * (x - self.mean)**2)


class InverseGammaNode(MetropolisNode):
    def __init__(self, name, alpha, beta, **kwargs):
        super().__init__(name, **kwargs)
        self._alpha = alpha
        self._beta = beta

    @property
    def alpha(self):
        return self.parameter(self._alpha)

    @property
    def beta(self):
        return self.parameter(self._beta)

    def sample(self, cand=None):
        cand = self.get_candidate_value()
        if cand <= 0:
            return self._val
        return super().sample(cand)

    def lookup_probability(self):
        x = self._val
        return self.alpha * np.log(self.beta) - gammaln(self.alpha) - ((self.alpha+1) * np.log(x)) - (self.beta/x)


class GammaNode(MetropolisNode):
    def __init__(self, name, alpha, beta, **kwargs):
        super().__init__(name, **kwargs)
        self._alpha = alpha
        self._beta = beta

    @property
    def alpha(self):
        return self.parameter(self._alpha)

    @property
    def beta(self):
        return self.parameter(self._beta)

    def sample(self, cand=None):
        cand = self.get_candidate_value()
        if cand <= 0:
            return self._val
        return super().sample(cand)

    def lookup_probability(self):
        x = self._val
        return self.alpha * np.log(self.beta) - gammaln(self.alpha) + ((self.alpha - 1) * np.log(x)) - (self.beta * x)


class BetaNode(MetropolisNode):
    def __init__(self, name, alpha, beta, **kwargs):
        super().__init__(name, **kwargs)
        self._alpha = alpha
        self._beta = beta

    @property
    def alpha(self):
        return self.parameter(self._alpha)

    @property
    def beta(self):
        return self.parameter(self._beta)

    def sample(self, cand=None):
        cand = self.get_candidate_value()
        if cand <= 0 or cand >= 1:
            return self._val
        return super().sample(cand)

    def lookup_probability(self):
        x = self._val
        alpha = self.alpha
        beta = self.beta
        return gammaln(alpha+beta) - gammaln(alpha) - gammaln(beta) + (alpha-1)*np.log(x) + (beta-1)*np.log(1-x)
