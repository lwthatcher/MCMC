
import argparse
from networks import *
from samples_loader import load_samples
import matplotlib.pyplot as plt
import matplotlib.pylab as mlab
import pickle


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
        j = 10
        for i in range(n_samples):
            samples.append(self.iteration())
            if i == j:
                print(i)
                j *= 10

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


def normal_expected_pdf(x):
    """Compute the Normal pdf at `x` given the priors."""
    mean = -.4
    var = .5
    return ((1 / (2 * math.pi * var) ** 0.5) *
        math.exp(-1 / (2 * var) * (x - mean) ** 2))


def gamma_expected_pdf(x):
    alpha = 5
    beta = 4
    return ((beta**alpha)/math.gamma(alpha)) * x**(alpha-1) * math.e**(-1 * beta * x)


def B(alpha, beta):
    return (math.gamma(alpha) * math.gamma(beta)) / math.gamma(alpha + beta)


def beta_pdf(x, alpha, beta):
    return ((x ** (alpha-1)) * ((1-x)**(beta-1))) / B(alpha, beta)


def beta_expected_t(x):
    return beta_pdf(x, 3, 3)


def beta_expected_f(x):
    return beta_pdf(x, 2, 4)


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
    graph.node_dict['G'].observed = True
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(20000, 2000000)
    with open('wacky_samples_G.pickle', 'wb') as ws:
        pickle.dump(samples, ws)
    with open('wacky_graph_G.pickle', 'wb') as wg:
        pickle.dump(graph, wg)
    for node in graph.nodes:
        mixing_plot(samples, node.name)
        plot_distribution(samples, node.name)


def load_wacky():
    samples = load_samples('wacky_samples.pickle')
    graph = load_samples('wacky_graph.pickle')
    for node in graph.nodes:
        mixing_plot(samples, node.name)
        plot_distribution(samples, node.name)


def load_golf():
    golfermean = load_samples('golf_samples.pickle')
    nsamples = len(golfermean)
    graph = golf()
    ability = []
    for golfer in graph.golfers:
        samples = [l[golfer] for l in golfermean]
        samples.sort()
        median = samples[nsamples // 2]
        low = samples[int(.05 * nsamples)]
        high = samples[int(.95 * nsamples)]
        ability.append((golfer, low, median, high))

    ability.sort(key=lambda x: x[2])
    i = 1
    for golfer, low, median, high in ability:
        print('%d: %s %f; 90%% interval: (%f, %f)' % (i, golfer, median, low, high))
        i += 1


def golfer_network_tests():
    graph = golf()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(1000, 100000)
    print('woohoo! the golfers finished!')
    with open('golf_samples.pickle', 'wb') as gs:
        pickle.dump(samples, gs)
    with open('golf_graph.pickle', 'wb') as gg:
        pickle.dump(graph, gg)


def normal_normal_tests():
    graph = normal_normal()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(500, 10000)
    plotposterior([s['A'] for s in samples], normal_expected_pdf, 'normal-normal', -2, 2)


def beta_bernoulli_tests():
    graph = beta_bernoulli()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(5000, 100000)
    plotposterior([s['A'] for s in samples], beta_expected_t, 'beta-bernoulli', 0, 1)

    graph = beta_bernoulli(b=0)
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(13000, 100000)
    plotposterior([s['A'] for s in samples], beta_expected_f, 'beta-bernoulli', 0, 1)


def gamma_poisson_tests():
    graph = gamma_poisson()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(50000, 10000)
    plotposterior([s['L'] for s in samples], gamma_expected_pdf, 'gamma-poisson', 0, 12)


def simple_bernoulli_tests():
    graph = bernoulli_simple()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(50, 10000)
    mean, f_mean = sample_dim(samples, 'B')
    print("P(B) = <", mean, ", ", f_mean, ">")


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
        elif test == 'normal_normal':
            normal_normal_tests()
        elif test == 'beta_bernoulli':
            beta_bernoulli_tests()
        elif test == 'simple_bernoulli':
            simple_bernoulli_tests()
        elif test == 'gamma_poisson':
            gamma_poisson_tests()
        elif test == 'sanity_checks':
            normal_normal_tests()
            beta_bernoulli_tests()
            gamma_poisson_tests()
        elif test == 'load_wacky':
            load_wacky()
        elif test == 'load_golf':
            load_golf()
        else:
            print('unrecognized test:', test)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tests', nargs='*')
    args = parser.parse_args()
    if args.tests:
        tests = args.tests
    else:
        tests = ['faculty_eval']
    main(tests)
