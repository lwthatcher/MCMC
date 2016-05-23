
class Graph:
    pass


class Node:

    def __init__(self, name, probs, graph=None, val=1, observed=False):
        self.name = name
        self._graph = graph
        self._probs = probs
        self._val = val
        self.observed = observed


def main():
    pass

if __name__ == '__main__':
    main()