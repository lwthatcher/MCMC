from collections import OrderedDict
from graph import *


def alarm():
    nodes = [BinaryNode('B', {(): 0.001}, val=0.),
             BinaryNode('E', {(): 0.002}, val=0.),
             BinaryNode('A', {(1, 1): 0.95, (1, 0): 0.94, (0, 1): 0.29, (0, 0): 0.001}, val=0.),
             BinaryNode('J', {(1,): 0.9, (0,): 0.05}, observed=True),
             BinaryNode('M', {(1,): 0.7, (0,): 0.01}, observed=True)]
    connections = OrderedDict([('B', ['A']),
                               ('E', ['A']),
                               ('A', ['J', 'M'])])
    return Graph(connections, nodes)


def burn():
    nodes = [BinaryNode('A', {(): 0.05}),
             BinaryNode('P', {(): 0.01}),
             BinaryNode('M', {(): 0.3}),
             BinaryNode('B', {(1, 1, 1): 0.9,
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
    nodes = [BinaryNode('Thomas', {(): 0.85}, val=1),
             BinaryNode('Percy', {(): 0.45}, val=1),
             BinaryNode('Diesel', {(): 0.3}, val=1, observed=True),
             BinaryNode('Diesel10', {(): 0.1}, val=1, observed=True),
             BinaryNode('BadAdvice', {(1, 1): 0.99, (1, 0): 0.89, (0, 1): 0.92, (0, 0): 0.2}, val=0.),
             BinaryNode('Fire', {(1,): 0.03, (0,): 0.001}),
             BinaryNode('ThomasRationalizes', {(1,): 0.6, (0,): 0.1}),
             BinaryNode('PercyRationalizes', {(1, 1): 0.2, (1, 0): 0.01, (0, 1): 0.5, (0, 0): 0.05}),
             BinaryNode('Accident', {(1, 1, 1): 0.87,
                               (1, 1, 0): 0.45,
                               (1, 0, 1): 0.5,
                               (1, 0, 0): 0.1,
                               (0, 1, 1): 0.32,
                               (0, 1, 0): 0.07,
                               (0, 0, 1): 0.2,
                               (0, 0, 0): 0.03}),
             BinaryNode('ReallyUseful', {(1, 1, 1): 0.2,
                                   (1, 1, 0): 0.9,
                                   (1, 0, 1): 0.05,
                                   (1, 0, 0): 0.6,
                                   (0, 1, 1): 0.03,
                                   (0, 1, 0): 0.55,
                                   (0, 0, 1): 0.03,
                                   (0, 0, 0): 0.5,}),
             BinaryNode('ConfusionDelay', {(1, 1): 0.999, (1, 0): 0.69, (0, 1): 0.9, (0, 0): 0.02}),
             BinaryNode('Cross', {(1, 1): 0.55, (1, 0): 0.01, (0, 1): 0.9, (0, 0): 0.15})]

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
    nodes = [BinaryNode('BC', {(): 0.68}),
             BinaryNode('SFB', {(): 0.5}),
             BinaryNode('AH', {(1,): 0.8, (0,): 0.7}),
             BinaryNode('AS', {(1,): 0.4, (0,): 0.6}),
             BinaryNode('IA', {(1, 1): 0.01, (1, 0): 0.24, (0, 1): 0.63, (0, 0): 0.95}, val=0., observed=True),
             BinaryNode('LO', {(1, 1): 0.96, (1, 0): 0.73, (0, 1): 0.14, (0, 0): 0.02}, val=0.)]
    connections = OrderedDict([('SFB', ['AH', 'AS']),
                               ('AH', ['IA']),
                               ('AS', ['IA']),
                               ('IA', ['LO']),
                               ('BC', ['LO'])])

    return Graph(connections, nodes)


def dirty_roommates():
    nodes = [BinaryNode('DR', {(): 0.7}, val=0., observed=True),
             BinaryNode('IT', {(): 0.8}),
             BinaryNode('CC', {(): 0.09}),
             BinaryNode('SDD', {(1, 1): 0.8, (1, 0): 0.4, (0, 1): 0.6, (0, 0): 0.9}, val=0.),
             BinaryNode('CK', {(1, 1): 0.99, (1, 0): 0.7, (0, 1): 0.5, (0, 0): 0.05}, val=1.)]
    connections = OrderedDict([('DR', ['SDD']),
                               ('IT', ['SDD']),
                               ('SDD', ['CK']),
                               ('CC', ['CK'])])

    return Graph(connections, nodes)


def faculty_evals():
    scores = [6.39,6.32,6.25,6.24,6.21,6.18,6.17,6.13,6.00,6.00,5.97,5.82,5.81,5.71,5.55,5.50,5.39,5.37,5.35,5.30,5.27,4.94,4.50]

    plate_nodes = [NormalNode('x' + str(i), 'mu', 'sigma2', val=score, observed=True) for i, score in enumerate(scores)]

    nodes = [NormalNode('mu', 5., 1/9, cand_var=0.2, val=5.),
             InverseGammaNode('sigma2', 11., 2.5, cand_var=0.15, val=0.3)] + plate_nodes

    connections = OrderedDict([('mu', ['x' + str(i) for i in range(len(scores))]),
                               ('sigma2', ['x' + str(i) for i in range(len(scores))])])

    return Graph(connections, nodes)