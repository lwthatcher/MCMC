import numpy as np
import math
from scipy.special import gammaln
import scipy.stats


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

    def __init__(self, name, graph=None, val=1, observed=False, hyper=False):
        self.name = name
        self._graph = graph
        self._val = val
        self.observed = observed
        self.hyper = hyper
        self._parents = None
        self._children = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return "(" + self.name + "=" + self.value + ")"

    def lookup_probability(self):
        return 0

    @property
    def parents(self):
        if self._parents is None:
            p = self._graph.inv_connections.get(self.name, [])
            self._parents = [self._graph.node_dict[n] for n in p]
        return self._parents

    @property
    def children(self):
        if self._children is None:
            c = self._graph.connections.get(self.name, [])
            self._children = [self._graph.node_dict[n] for n in c]
        return self._children

    @property
    def value(self):
        return str(self._val)


class BinaryNode(Node):

    def __init__(self, name, probs, **kwargs):
        super().__init__(name, **kwargs)
        if isinstance(probs, BernoulliParam):
            self._probs = probs
        else:
            self._probs = BernoulliTable(probs, self)

    def lookup_probability(self):
        given = self._parent_values()
        prob = self._probs[given]
        if self._val == 1:
            return np.log(prob)
        else:
            return np.log(1.0 - prob)

    def _parent_values(self):
        l = [p._val for p in self.parents if not p.hyper]
        return tuple(l)

    def sample(self):
        self._val = 1
        pos = self.lookup_probability()
        for child in self.children:
            pos += child.lookup_probability()

        self._val = 0
        neg = self.lookup_probability()
        for child in self.children:
            neg += child.lookup_probability()

        p = pos - np.logaddexp(pos, neg)
        out = np.random.binomial(1, np.exp(p))
        self._val = out
        return out

    @property
    def value(self):
        if self._val == 1:
            return 't'
        else:
            return 'f'


class BernoulliTable:
    def __init__(self, probs, node):
        self.probs = probs
        self.node = node

    def __getitem__(self, item):
        x = self.probs[item]
        if isinstance(x, Node):
            return x._val
        if isinstance(x, str):
            node = self.node._graph.node_dict[x]
            self.probs[item] = node
            return node._val
        else:
            return x


class BernoulliParam:

    def __getitem__(self, item):
        return item[0]


class Param:
    def __init__(self, func, *args):
        self._func = func
        self._args = args

    def __call__(self, graph):
        nodes = [graph.node_dict[name] for name in self._args]
        return self._func(*nodes)


class BernoulliNode(Node):
    def __init__(self, name, prob, **kwargs):
        super().__init__(name, **kwargs)
        self._prob = prob

    def lookup_probability(self):
        prob = self.parameter(self._prob)
        if self._val == 1:
            return prob
        else:
            return 1 - prob

    def parameter(self, param):
        if isinstance(param, Node):
            return param._val
        elif isinstance(param, str):
            return self._graph.node_dict[param]._val
        elif isinstance(param, Param):
            return param(self._graph)
        else:
            return param

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
        elif isinstance(param, Param):
            return param(self._graph)
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

    def get_candidate_value(self):
        return scipy.stats.beta.rvs(1, 1)

    @property
    def alpha(self):
        return self.parameter(self._alpha)

    @property
    def beta(self):
        return self.parameter(self._beta)

    def sample(self, cand=None):
        cand = self.get_candidate_value()
        if cand <= 0 or cand > 1:
            return self._val
        return super().sample(cand)

    def lookup_probability(self):
        x = self._val
        alpha = self.alpha
        beta = self.beta
        return gammaln(alpha+beta) - gammaln(alpha) - gammaln(beta) + (alpha-1)*np.log(x) + (beta-1)*np.log(1-x)


class UniformNode(MetropolisNode):
    def __init__(self, name, theta, discrete=False, **kwargs):
        super().__init__(name, **kwargs)
        self._theta = theta
        self.discrete = discrete

    def get_candidate_value(self):
        r = np.random.uniform(0, self.theta)
        if self.discrete:
            r = round(r)
        return r

    @property
    def theta(self):
        return self.parameter(self._theta)

    def lookup_probability(self):
        if self._val > self.theta:
            return 0
        result = -1 * np.log(self.theta)
        return result


class ParetoNode(MetropolisNode):
    def __init__(self, name, alpha, x_0, **kwargs):
        super().__init__(name, **kwargs)
        self._alpha = alpha
        self._x_0 = x_0

    @property
    def alpha(self):
        return self.parameter(self._alpha)

    @property
    def x_0(self):
        return self.parameter(self._x_0)

    def sample(self, cand=None):
        cand = self.get_candidate_value()
        if cand < self.x_0:
            return self._val
        return super().sample(cand)

    def lookup_probability(self):
        x = self._val
        if x < self.x_0:
            return 0
        return np.log(self.alpha) + self.alpha*np.log(self.x_0) - (self.alpha+1)*np.log(x)


class PoissonNode(MetropolisNode):
    def __init__(self, name, theta, **kwargs):
        super().__init__(name, **kwargs)
        self._theta = theta

    @property
    def theta(self):
        return self.parameter(self._theta)

    def sample(self, cand=None):
        cand = self.get_candidate_value()
        if cand <= 0:
            return self._val
        return super().sample(cand)

    def get_candidate_value(self):
        mu = self._val
        sigma = math.sqrt(self.cd_var)
        return round(np.random.normal(mu, sigma))

    def lookup_probability(self):
        x = float(self._val)
        return x*np.log(self.theta) - gammaln(x+1.) - self.theta