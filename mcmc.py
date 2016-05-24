
import numpy as np
from networks import alarm
from networks import burn
from networks import thomas

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


def main():
    mcmc = MCMC()
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")
    mean, f_mean = sample_dim(samples, 'A')
    print("P(Alarm | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")
    mean, f_mean = sample_dim(samples, 'E')
    print("P(Earthquake | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'J':1., 'M':0.})
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

    graph = burn()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'M')
    print("P(MapoDoufu | Burn=false) = <", mean, ", ", f_mean, ">")

    graph = thomas()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = sample_dim(samples, 'M')
    print("P(Cross | Thomas=true, Percy=true, Diesel=true) = <", mean, ", ", f_mean, ">")


if __name__ == '__main__':
    main()
