from mcmc import MCMC
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as mlab
import matplotlib.patches as mpatches
import matplotlib.colors
import argparse
from networks import *
import pickle
import json
import math
from samples_loader import load_samples


def alarm_tests():
    mcmc = MCMC()
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")
    mean, f_mean = Tests.sample_dim(samples, 'A')
    print("P(Alarm | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")
    mean, f_mean = Tests.sample_dim(samples, 'E')
    print("P(Earthquake | JohnCalls=true, MaryCalls=true) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'J': 1., 'M': 0.})
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true, MaryCalls=false) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'J': 1.})
    mcmc.graph.node_dict['M'].observed = False
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'B')
    print("P(Burglary | JohnCalls=true) = <", mean, ", ", f_mean, ">")

    mcmc = MCMC({'M': 1.})
    mcmc.graph.node_dict['J'].observed = False
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'B')
    print("P(Burglary | MaryCalls=true) = <", mean, ", ", f_mean, ">")
    print()


def burn_tests():
    graph = burn()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'M')
    print("P(MapoDoufu | Burn=false) = <", mean, ", ", f_mean, ">")
    print()


def thomas_tests():
    graph = thomas()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'Cross')
    print("P(Cross | Diesel=true, Diesel10=true) = <", mean, ", ", f_mean, ">")

    graph = thomas()
    graph.node_dict['Diesel'].observed = False
    graph.node_dict['Diesel10'].observed = False
    graph.node_dict['Thomas'].observed = True
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'Cross')
    print("P(Cross | Thomas=true) = <", mean, ", ", f_mean, ">")

    graph = thomas()
    graph.node_dict['Diesel'].observed = False
    graph.node_dict['Diesel10'].observed = False
    graph.node_dict['Cross'].observed = True
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'Diesel')
    print("P(Diesel | Cross=true) = <", mean, ", ", f_mean, ">")
    print()


def home_or_school_tests():
    graph = home_or_school()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'AS')
    print("P(AS | IA=false) = <", mean, ", ", f_mean, ">")

    graph = home_or_school()
    mcmc = MCMC({'IA': 1}, graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'AS')
    print("P(AS | IA=false) = <", mean, ", ", f_mean, ">")
    print()


def dirty_roommates_tests():
    graph = dirty_roommates()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'CK')
    print("P(CK | DR=false) = <", mean, ", ", f_mean, ">")

    graph = dirty_roommates()
    graph.node_dict['DR'].observed = False
    graph.node_dict['CK'].observed = True
    mcmc = MCMC({'CK': 1}, graph=graph)
    samples = mcmc.gibbs(10000, 10000)
    mean, f_mean = Tests.sample_dim(samples, 'IT')
    print("P(IT | CK=true) = <", mean, ", ", f_mean, ">")


def faculty_evaluation_tests():
    graph = faculty_evals()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(500, 10000)
    Tests.mixing_plot(samples, 'mu')
    Tests.mixing_plot(samples, 'sigma2')
    Tests.plotposterior([s['mu'] for s in samples], faculty_mean_prior, 'mean', 5.0, 6.5)
    Tests.plotposterior([s['sigma2'] for s in samples], faculty_var_prior, 'var', 0.0001, 1.0)


def hyper_faculty_tests():
    meta_samples = []
    for n in range(5):
        graph = faculty_evals_1hyper(n)
        mcmc = MCMC(graph=graph)
        samples = mcmc.gibbs(10000, 100000)
        print(n)
        Tests.plot_multi(samples, ['mu', 'sigma2'])
        print(graph.nodes)
        for node in graph.hidden_nodes:
            if node.name != 'mu' and node.name != 'sigma2':
                Tests.mixing_plot(samples, node.name)
                Tests.plot_distribution(samples, node.name)


def wacky_network_tests():
    graph = wacky()
    # graph.node_dict['G'].observed = True
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(20000, 2000000)
    with open('wacky_G_samples.pickle', 'wb') as ws:
        pickle.dump(samples, ws)
    with open('wacky_G_graph.pickle', 'wb') as wg:
        pickle.dump(graph, wg)
    for node in graph.nodes:
        Tests.mixing_plot(samples, node.name)
        Tests.plot_distribution(samples, node.name)


def load_wacky():
    samples = load_samples('wacky_samples.pickle')
    graph = load_samples('wacky_graph.pickle')
    for node in graph.nodes:
        Tests.mixing_plot(samples, node.name)
        Tests.plot_distribution(samples, node.name)


def load_wacky_G():
    samples = load_samples('wacky_G_samples.pickle')
    graph = load_samples('wacky_G_graph.pickle')
    for node in graph.hidden_nodes:
        Tests.mixing_plot(samples, node.name)
        Tests.plot_distribution(samples, node.name)


def golfer_network_tests():
    graph = golf()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(1000, 100000)
    print('woohoo! the golfers finished!')
    with open('golf_samples.pickle', 'wb') as gs:
        pickle.dump(samples, gs)
    with open('golf_graph.pickle', 'wb') as gg:
        pickle.dump(graph, gg)


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


def normal_normal_tests():
    graph = normal_normal()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(500, 10000)
    Tests.plotposterior([s['A'] for s in samples], normal_expected, 'normal-normal', -3, 3)


def beta_bernoulli_tests():
    graph = beta_bernoulli()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(5000, 100000)
    Tests.plotposterior([s['A'] for s in samples], beta_expected_t, 'beta-bernoulli', 0, 1)

    graph = beta_bernoulli(b=0)
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(13000, 100000)
    Tests.plotposterior([s['A'] for s in samples], beta_expected_f, 'beta-bernoulli', 0, 1)


def gamma_poisson_tests():
    graph = gamma_poisson()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(50000, 10000)
    Tests.plotposterior([s['L'] for s in samples], gamma_expected, 'gamma-poisson', 0, 12)


def tanks_tests():
    graph = tanks()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(50, 100000)
    Tests.mixing_plot(samples, 'num_tanks')
    Tests.plot_distribution(samples, 'num_tanks')
    Tests.mixing_plot(samples, 'A')
    Tests.plot_distribution(samples, 'A')


def progress_tests():
    graph = progress()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(2000, 50000)
    Tests.plot_distribution(samples, 'Encounters')
    encounters = [s['Encounters'] for s in samples]
    median = np.median(encounters)
    print('median', median)


def pareto_poisson_tests():
    graph = pareto()
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(2000, 100000)
    for node in graph.hidden_nodes:
        #Tests.mixing_plot(samples, node.name)
        Tests.plot_distribution(samples, node.name)
        encounters = [s[node.name] for s in samples]
        median = np.median(encounters)
        print('median', median)


def hyper_alarm_generate():
    val_dict = 'orig'
    graph = hyper_alarm(val_dict)
    mcmc = MCMC(graph=graph)
    samples = mcmc.gibbs(10000, 30000)
    mean, f_mean = Tests.sample_dim(samples, 'B')
    print(mean, f_mean)
    mean, f_mean = Tests.sample_dim(samples, 'E')
    print(mean, f_mean)

    saved_samples = []
    for i, sample in enumerate(samples):
        if i < 3001 and i % 3 == 0:
            #print(sample)
            saved_samples.append(sample)
    with open('alarm-gen-lab.json', 'w') as f:
        json.dump(saved_samples,f)


def hyper_alarm_learning_tests():
    legs = [10, 25, 50, 75, 100, 250, 500, 750, 1000]
    for n in legs:
        graph = hyper_alarm_learn('alarm-gen-lab.json', n=n)
        mcmc = MCMC(graph=graph)
        samples = mcmc.gibbs(1000, 1000)
        mean, f_mean = Tests.sample_dim(samples, 'b_B')
        print(mean, f_mean)
        mean, f_mean = Tests.sample_dim(samples, 'b_E')
        print(mean, f_mean)
        name = 'alarm-lab_' + str(n) + '_samples.pickle'
        with open(name, 'wb') as f:
            pickle.dump(samples, f)


def load_hyper_alarm():
    legs = [10, 25, 50, 75, 100, 250, 500, 750, 1000]
    model = '01'
    with open('alarm-expected-' + model + '.json', 'r') as f:
        expected = json.load(f)
    for n in legs:
        print('n = ', n)
        name = 'alarm-' + model + '_' + str(n) + '_samples.pickle'
        samples = load_samples(name)
        accuracies = []
        mean, f_mean = Tests.sample_dim(samples, 'b_B')
        print('P(B=t) = ', mean)
        accuracies.append(expected['b_B'] - mean)
        mean, f_mean = Tests.sample_dim(samples, 'b_E')
        print('P(E=t) = ', mean)
        accuracies.append(expected['b_E'] - mean)

        mean, f_mean = Tests.sample_dim(samples, 'b_A_11')
        print('P(A=t | B=t, E=t) = ', mean)
        accuracies.append(expected['b_A_11'] - mean)
        mean, f_mean = Tests.sample_dim(samples, 'b_A_10')
        print('P(A=t | B=t, E=f) = ', mean)
        accuracies.append(expected['b_A_10'] - mean)
        mean, f_mean = Tests.sample_dim(samples, 'b_A_01')
        print('P(A=t | B=f, E=t) = ', mean)
        accuracies.append(expected['b_A_01'] - mean)
        mean, f_mean = Tests.sample_dim(samples, 'b_A_00')
        print('P(A=t | B=f, E=f) = ', mean)
        accuracies.append(expected['b_A_00'] - mean)

        mean, f_mean = Tests.sample_dim(samples, 'b_J_1')
        print('P(J=t | A=t) = ', mean)
        accuracies.append(expected['b_J_1'] - mean)
        mean, f_mean = Tests.sample_dim(samples, 'b_J_0')
        print('P(J=t | A=f) = ', mean)
        accuracies.append(expected['b_J_0'] - mean)

        mean, f_mean = Tests.sample_dim(samples, 'b_M_1')
        print('P(M=t | A=t) = ', mean)
        accuracies.append(expected['b_M_1'] - mean)
        mean, f_mean = Tests.sample_dim(samples, 'b_M_0')
        print('P(M=t | A=f) = ', mean)
        accuracies.append(expected['b_M_0'] - mean)
        print()
        total = 0
        for a in accuracies:
            total += abs(a)
        print('accuracy = ', 1 - (total / len(accuracies)))
        print()
        print()


def faculty_mean_prior(x):
    return Tests.normal_pdf(x, 5, 1 / 9)


def faculty_var_prior(x):
    return Tests.inverse_gamma_pdf(x, 11, 2.5)


def normal_expected(x):
    return Tests.normal_pdf(x, -.4, .5)


def beta_expected_t(x):
    return Tests.beta_pdf(x, 3, 3)


def beta_expected_f(x):
    return Tests.beta_pdf(x, 2, 4)


def gamma_expected(x):
    return Tests.gamma_pdf(x, 5, 4)


class Tests:
    def __init__(self):
        self.test_dict = {'alarm': alarm_tests,
                          'lab1': [alarm_tests, burn_tests, thomas_tests, home_or_school_tests, dirty_roommates_tests],
                          'faculty': faculty_evaluation_tests,
                          'wacky': wacky_network_tests,
                          'load_wacky': load_wacky,
                          'load_wacky_G': load_wacky_G,
                          'golf': golfer_network_tests,
                          'load_golf': load_golf,
                          'normal-normal': normal_normal_tests,
                          'beta-bernoulli': beta_bernoulli_tests,
                          'gamma-poisson': gamma_poisson_tests,
                          'sanity_checks': [normal_normal_tests, beta_bernoulli_tests, gamma_poisson_tests],
                          'tanks': tanks_tests,
                          'progress': progress_tests,
                          'pareto-poisson': pareto_poisson_tests,
                          'faculty-hyper': hyper_faculty_tests,
                          'alarm-hyper-gen': hyper_alarm_generate,
                          'alarm-hyper-learn': hyper_alarm_learning_tests,
                          'alarm-hyper-load': load_hyper_alarm}

    def perform_tests(self, tests):
        for test in tests:
            if test in self.test_dict:
                if isinstance(test, list):
                    for t in self.test_dict[test]:
                        t()
                else:
                    t = self.test_dict[test]
                    t()
            else:
                print('unrecognized test:', test)

    @classmethod
    def mixing_plot(cls, samples, dim):
        xs, ys = zip(*enumerate([s[dim] for s in samples]))
        plt.plot(xs, ys)
        plt.title('{} mixing'.format(dim))
        plt.show()

    @classmethod
    def plotposterior(cls, samples, prior_pdf, name, xmin, xmax):
        xs = mlab.frange(xmin, xmax, (xmax - xmin) / 100)
        ys = [prior_pdf(x) for x in xs]
        plt.plot(xs, ys, label='Prior Dist')

        plt.hist(samples, bins=30, normed=True, label='Posterior Dist')

        plt.title('Prior and Posterior of {}'.format(name))
        plt.ylim(ymin=0)
        plt.xlim(xmin, xmax)
        plt.show()

    @classmethod
    def plot_distribution(cls, samples, dim):
        samples = [s[dim] for s in samples]
        plt.hist(samples, bins=40, normed=True, label='Posterior Dist')
        plt.title('Posterior Distribution of {}'.format(dim))
        plt.show()

    @classmethod
    def plot_multi(cls, samples, dims):
        color_list = matplotlib.colors.ColorConverter.colors
        it = iter(sorted(color_list.items()))
        fig, ax = plt.subplots()
        axes = [ax]
        axes += [ax.twiny() for i in range(len(dims)-1)]
        patches = []
        for i, dim in enumerate(dims):
            x = [s[dim] for s in samples]
            c = next(it)[1]
            axx = axes[i]
            axx.hist(x, bins=40, normed=True, label=dim, color=c, alpha=0.5)
            patch = mpatches.Patch(color=c, label=dim, alpha=0.5)
            patches.append(patch)
        plt.legend(handles=patches)
        plt.show()

    @classmethod
    def sample_dim(cls, samples, dim):
        d = [s[dim] for s in samples]
        true_mean = np.mean(d)
        false_mean = 1 - true_mean
        return true_mean, false_mean

    # PDFs
    @classmethod
    def normal_pdf(cls, x, mean, var):
        return ((1 / (2 * math.pi * var) ** 0.5) *
                math.exp(-1 / (2 * var) * (x - mean) ** 2))

    @classmethod
    def inverse_gamma_pdf(cls, x, alpha, beta):
        return beta ** alpha / math.gamma(alpha) * x ** (-alpha - 1) * math.exp(-beta / x)

    @classmethod
    def beta_pdf(cls, x, alpha, beta):
        return ((x ** (alpha - 1)) * ((1 - x) ** (beta - 1))) / cls.B(alpha, beta)

    @classmethod
    def gamma_pdf(cls, x, alpha, beta):
        return ((beta ** alpha) / math.gamma(alpha)) * x ** (alpha - 1) * math.e ** (-1 * beta * x)

    @staticmethod
    def B(alpha, beta):
        return (math.gamma(alpha) * math.gamma(beta)) / math.gamma(alpha + beta)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tests', nargs='*')
    args = parser.parse_args()
    if args.tests:
        _tests = args.tests
    else:
        _tests = ['alarm']
    tester = Tests()
    tester.perform_tests(_tests)