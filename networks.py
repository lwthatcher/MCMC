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


def thomas():
    nodes = [Node('Thomas', {(): 0.85}, val=1),
             Node('Percy', {(): 0.45}, val=1),
             Node('Diesel', {(): 0.3}, val=1, observed=True),
             Node('Diesel10', {(): 0.1}, val=1, observed=True),
             Node('BadAdvice', {(1, 1): 0.99, (1, 0): 0.89, (0, 1): 0.92, (0, 0): 0.2}, val=0.),
             Node('Fire', {(1,): 0.03, (0,): 0.001}),
             Node('ThomasRationalizes', {(1,): 0.6, (0,): 0.1}),
             Node('PercyRationalizes', {(1, 1): 0.2, (1, 0): 0.01, (0, 1): 0.5, (0, 0): 0.05}),
             Node('Accident', {(1, 1, 1): 0.87,
                               (1, 1, 0): 0.45,
                               (1, 0, 1): 0.5,
                               (1, 0, 0): 0.1,
                               (0, 1, 1): 0.32,
                               (0, 1, 0): 0.07,
                               (0, 0, 1): 0.2,
                               (0, 0, 0): 0.03}),
             Node('ReallyUseful', {(1, 1, 1): 0.2,
                                   (1, 1, 0): 0.9,
                                   (1, 0, 1): 0.05,
                                   (1, 0, 0): 0.6,
                                   (0, 1, 1): 0.03,
                                   (0, 1, 0): 0.55,
                                   (0, 0, 1): 0.03,
                                   (0, 0, 0): 0.5,}),
             Node('ConfusionDelay', {(1, 1): 0.999, (1, 0): 0.69, (0, 1): 0.9, (0, 0): 0.02}),
             Node('Cross', {(1, 1): 0.55, (1, 0): 0.01, (0, 1): 0.9, (0, 0): 0.15})]

    connections = OrderedDict([('Thomas', ['PercyRationalizes', 'ReallyUseful']),
                               ('Percy', ['ReallyUseful']),
                               ('BadAdvice', ['ThomasRationalizes', 'PercyRationalizes']),
                               ('ThomasRationalizes', ['Accident']),
                               ('PercyRationalizes', ['Accident']),
                               ('Diesel', ['BadAdvice', 'Accident']),
                               ('Diesel10', ['BadAdvice', 'Fire']),
                               ('Accident', ['ReallyUseful', 'ConfusionDelay']),
                               ('Fire', ['ConfusionDelay']),
                               ('ReallyUseful', ['Cross']),
                               ('ConfusionDelay', ['Cross'])])

    return Graph(connections, nodes)
