
from networks import *


class MCMC:

    def __init__(self, obs=None, graph=None):
        if graph is None:
            graph = alarm()
        self.graph = graph
        if obs is not None:
            for node in obs:
                self.graph.node_dict[node]._val = obs[node]

    def iteration(self):
        result = {}
        for node in self.graph.hidden_nodes:
            xi = node.sample()
            result[node.name] = xi
        return result

    def gibbs(self, burn, n_samples):
        # burn period
        for i in range(burn):
            self.iteration()
        # take n samples
        samples = []
        for i in range(n_samples):
            samples.append(self.iteration())

        return samples
