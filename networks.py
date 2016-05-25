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


def home_or_school():
    nodes = [Node('BC', {(): 0.68}),
             Node('SFB', {(): 0.5}),
             Node('AH', {(1,): 0.8, (0,): 0.7}),
             Node('AS', {(1,): 0.4, (0,): 0.6}),
             Node('IA', {(1, 1): 0.01, (1, 0): 0.24, (0, 1): 0.63, (0, 0): 0.95}, val=0., observed=True),
             Node('LO', {(1, 1): 0.96, (1, 0): 0.73, (0, 1): 0.14, (0, 0): 0.02}, val=0.)]
    connections = OrderedDict([('SFB', ['AH', 'AS']),
                               ('AH', ['IA']),
                               ('AS', ['IA']),
                               ('IA', ['LO']),
                               ('BC', ['LO'])])

    return Graph(connections, nodes)


def dirty_roommates():
    nodes = [Node('DR', {(): 0.7}, val=0., observed=True),
             Node('IT', {(): 0.8}),
             Node('CC', {(): 0.09}),
             Node('SDD', {(1, 1): 0.8, (1, 0): 0.4, (0, 1): 0.6, (0, 0): 0.9}, val=0.),
             Node('CK', {(1, 1): 0.99, (1, 0): 0.7, (0, 1): 0.5, (0, 0): 0.05}, val=1.)]
    connections = OrderedDict([('DR', ['SDD']),
                               ('IT', ['SDD']),
                               ('SDD', ['CK']),
                               ('CC', ['CK'])])

    return Graph(connections, nodes)
