
from burglar_alarm import alarm


class MCMC:

    def __init__(self):
        self.graph = alarm()

    def iteration(self):
        result = []
        for node in self.graph.hidden_nodes:
            xi = node.sample()
            result.append(xi)
        return result

    def gibbs(self, burn, n_samples):
        # burn period
        for i in range(burn):
            self.iteration()
        # take n samples
        samples = [self.iteration() for i in range(n_samples)]

        print(samples)


def main():
    mcmc = MCMC()
    mcmc.gibbs(1, 1000)

if __name__ == '__main__':
    main()