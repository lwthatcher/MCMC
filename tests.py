from mcmc import MCMC
import numpy as np
import argparse


def alarm_tests():
    mcmc = MCMC()
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = MCMCTests.sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")
    mean, f_mean = MCMCTests.sample_dim(samples, 'A')
    print("P(Alarm | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")
    mean, f_mean = MCMCTests.sample_dim(samples, 'E')
    print("P(Earthquake | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'J': 1., 'M': 0.})
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = MCMCTests.sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true, MaryCalls=false) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'J': 1.})
    mcmc.graph.node_dict['M'].observed = False
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = MCMCTests.sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'M': 1.})
    mcmc.graph.node_dict['J'].observed = False
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = MCMCTests.sample_dim(samples, 'B')
    print("P(Burglary | MaryCalls=true) = <", mean, ", ", f_mean, ">")
    print()


class MCMCTests:

    def __init__(self):
        self.test_dict = {'alarm': alarm_tests}

    def perform_tests(self, tests):
        for test in tests:
            if test in self.test_dict:
                t = self.test_dict[test]
                t()
            else:
                print('unrecognized test:', test)

    @classmethod
    def sample_dim(cls, samples, dim):
        d = [s[dim] for s in samples]
        true_mean = np.mean(d)
        false_mean = 1 - true_mean
        return true_mean, false_mean


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tests', nargs='*')
    args = parser.parse_args()
    if args.tests:
        _tests = args.tests
    else:
        _tests = ['alarm']
    tester = MCMCTests()
    tester.perform_tests(_tests)