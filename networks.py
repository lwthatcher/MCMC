
from collections import OrderedDict
from graph import Graph
from graph import Node


def alarm():
    nodes = [Node('B', {(): 0.001}, val=0.),
             Node('E', {(): 0.002}, val=0.),
             Node('A', {(1, 1): 0.95, (1, 0): 0.94, (0, 1): 0.29, (0, 0): 0.001}, val=0.),
             Node('J', {(1,): 0.9, (0,): 0.05}, observed=True),
             Node('M', {(1,): 0.7, (0,): 0.01}, observed=True)]
    connections = OrderedDict([('B', ['A']),
                               ('E', ['A']),
                                ('A', ['J', 'M'])])
    return Graph(connections, nodes)


def burn():
    nodes = [Node('A', {(): 0.05}),
             Node('P', {(): 0.01}),
             Node('M', {(): 0.3}),
             Node('B', {(1, 1, 1): 0.9,
                        (1, 1, 0): 0.8,
                        (1, 0, 1): 0.7,
                        (1, 0, 0): 0.3,
                        (0, 1, 1): 0.55,
                        (0, 1, 0): 0.5,
                        (0, 0, 1): 0.9,
                        (0, 0, 0): 0.9,}, observed=True, val=0.)]

    connections = OrderedDict([('A', ['B']),
                               ('P', ['B']),
                               ('M', ['B'])])
    return Graph(connections, nodes)
