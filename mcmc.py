
import numpy as np
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
        samples = [self.iteration() for i in range(n_samples)]

        return samples


def sample_dim(samples, dim):
    d = [s[dim] for s in samples]
    true_mean = np.mean(d)
    false_mean = 1 - true_mean
    return true_mean, false_mean


def lab1_tests():
    mcmc = MCMC()
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")
    mean, f_mean = sample_dim(samples, 'A')
    print("P(Alarm | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")
    mean, f_mean = sample_dim(samples, 'E')
    print("P(Earthquake | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'J': 1., 'M': 0.})
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true, MaryCalls=false) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'J': 1.})
    mcmc.graph.node_dict['M'].observed = False
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'M': 1.})
    mcmc.graph.node_dict['J'].observed = False
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'B')
    print("P(Burglary | MaryCalls=true) = <", mean, ", ", f_mean, ">")
    print()

    graph = burn()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'M')
    print("P(MapoDoufu | Burn=false) = <", mean, ", ", f_mean, ">")
    print()

    graph = thomas()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'Cross')
    print("P(Cross | Diesel=true, Diesel10=true) = <", mean, ", ", f_mean, ">")

    graph = thomas()
    graph.node_dict['Diesel'].observed = False
    graph.node_dict['Diesel10'].observed = False
    graph.node_dict['Thomas'].observed = True
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'Cross')
    print("P(Cross | Thomas=true) = <", mean, ", ", f_mean, ">")

    graph = thomas()
    graph.node_dict['Diesel'].observed = False
    graph.node_dict['Diesel10'].observed = False
    graph.node_dict['Cross'].observed = True
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'Diesel')
    print("P(Diesel | Cross=true) = <", mean, ", ", f_mean, ">")
    print()

    graph = home_or_school()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'AS')
    print("P(AS | IA=false) = <", mean, ", ", f_mean, ">")

    graph = home_or_school()
    mcmc = MCMC({'IA': 1}, graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'AS')
    print("P(AS | IA=false) = <", mean, ", ", f_mean, ">")
    print()

    graph = dirty_roommates()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'CK')
    print("P(CK | DR=false) = <", mean, ", ", f_mean, ">")

    graph = dirty_roommates()
    graph.node_dict['DR'].observed = False
    graph.node_dict['CK'].observed = True
    mcmc = MCMC({'CK': 1}, graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'IT')
    print("P(IT | CK=true) = <", mean, ", ", f_mean, ">")


def main():
    lab1_tests()


if __name__ == '__main__':
    main()
