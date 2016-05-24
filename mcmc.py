
import numpy as np
from burglar_alarm import alarm


class MCMC:

    def __init__(self):
        self.graph = alarm()

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


if __name__ == '__main__':
    main()
