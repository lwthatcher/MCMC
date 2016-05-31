
import argparse
from networks import *
import matplotlib.pyplot as plt
import matplotlib.pylab as mlab


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


def mixing_plot(samples, dim):
    xs, ys = zip(*enumerate([s[dim] for s in samples]))
    plt.plot(xs, ys)
    plt.title('{} mixing'.format(dim))
    plt.show()


def mean_prior_pdf(x):
    """Compute the Normal pdf at `x` given the priors."""
    mean = 5
    var = 1/9
    return ((1 / (2 * math.pi * var) ** 0.5) *
        math.exp(-1 / (2 * var) * (x - mean) ** 2))


def var_prior_pdf(x):
    """Compute the Inverse Gamma pdf at `x` given the priors.

    Note that we use the scale parameterization of `beta`.
    """
    alpha = 11
    beta = 2.5
    return beta ** alpha / math.gamma(alpha) * x**(-alpha - 1) * math.exp(-beta / x)


def plotposterior(samples, prior_pdf, name, xmin, xmax):
    xs = mlab.frange(xmin, xmax, (xmax-xmin) / 100)
    ys = [prior_pdf(x) for x in xs]
    plt.plot(xs, ys, label='Prior Dist')

    plt.hist(samples, bins=30, normed=True, label='Posterior Dist')

    plt.title('Prior and Posterior of {}'.format(name))
    plt.ylim(ymin=0)
    plt.xlim(xmin, xmax)
    plt.show()


def plot_distribution(samples, dim):
    samples = [s[dim] for s in samples]
    plt.hist(samples, bins=40, normed=True, label='Posterior Dist')
    plt.title('Posterior Distribution of {}'.format(dim))
    plt.show()


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


def faculty_evaluation_tests():
    graph = faculty_evals()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(50, 10000)
    mixing_plot(samples, 'mu')
    mixing_plot(samples, 'sigma2')
    plotposterior([s['mu'] for s in samples], mean_prior_pdf, 'mean', 5.0, 6.5)
    plotposterior([s['sigma2'] for s in samples], var_prior_pdf, 'var', 0.0001, 1.0)


def wacky_network_tests():
    graph = wacky()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(100000, 10000)
    for node in graph.nodes:
        mixing_plot(samples, node.name)
        plot_distribution(samples, node.name)


def golfer_network_tests():
    graph = golf()
    mcmc = MCMC(graph=graph)


def main(_tests):
    for test in _tests:
        if test == 'lab1':
            lab1_tests()
        elif test == 'faculty_eval':
            faculty_evaluation_tests()
        elif test == 'wacky':
            wacky_network_tests()
        elif test == 'golf':
            golfer_network_tests()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tests', nargs='*')
    args = parser.parse_args()
    if args.tests:
        tests = args.tests
    else:
        tests = ['faculty_eval']
    main(tests)
