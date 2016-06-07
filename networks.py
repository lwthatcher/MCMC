import random
from collections import OrderedDict
from graph import *
import csv
import json


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


def hyper_alarm(val_dict=None):
    if val_dict is None:
        val_dict = 'lab'
    val_dict = 'alarm-expected-' + val_dict + '.json'
    with open(val_dict, 'r') as f:
        vals = json.load(f)

    nodes = [BetaNode('b_B', 1, 1, val=vals['b_B'], observed=True, hyper=True),
             BetaNode('b_E', 1, 1, val=vals['b_E'], observed=True, hyper=True),
             BetaNode('b_A_11', 1, 1, val=vals['b_A_11'], observed=True, hyper=True),
             BetaNode('b_A_10', 1, 1, val=vals['b_A_10'], observed=True, hyper=True),
             BetaNode('b_A_01', 1, 1, val=vals['b_A_01'], observed=True, hyper=True),
             BetaNode('b_A_00', 1, 1, val=vals['b_A_00'], observed=True, hyper=True),
             BetaNode('b_J_1', 1, 1, val=vals['b_J_1'], observed=True, hyper=True),
             BetaNode('b_J_0', 1, 1, val=vals['b_J_0'], observed=True, hyper=True),
             BetaNode('b_M_1', 1, 1, val=vals['b_M_1'], observed=True, hyper=True),
             BetaNode('b_M_0', 1, 1, val=vals['b_M_0'], observed=True, hyper=True),
             BinaryNode('B', {(): 'b_B'}, val=0.),
             BinaryNode('E', {(): 'b_E'}, val=0.),
             BinaryNode('A', {(1, 1): 'b_A_11', (1, 0): 'b_A_10', (0, 1): 'b_A_01', (0, 0): 'b_A_00'}, val=0.),
             BinaryNode('J', {(1,): 'b_J_1', (0,): 'b_J_0'}),
             BinaryNode('M', {(1,): 'b_M_1', (0,): 'b_M_0'})]
    connections = OrderedDict([('B', ['A']),
                               ('E', ['A']),
                               ('A', ['J', 'M']),
                               ('b_B', ['B']),
                               ('b_E', ['E']),
                               ('b_A_11', ['A']),
                               ('b_A_10', ['A']),
                               ('b_A_01', ['A']),
                               ('b_A_00', ['A']),
                               ('b_J_1', ['J']),
                               ('b_J_0', ['J']),
                               ('b_M_1', ['M']),
                               ('b_M_0', ['M'])])
    return Graph(connections, nodes)


# noinspection PyTypeChecker
def hyper_alarm_learn(observations=None, n=1000, val_dict=None, inference=False):
    if val_dict is None:
        val_dict = 'orig'
    val_dict = 'alarm-expected-' + val_dict + '.json'
    with open(val_dict, 'r') as f:
        vals = json.load(f)

    _obs = [{'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 1, 'B': 0, 'E': 0, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 1, 'E': 0, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 1, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 1, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 0, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 0, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 1, 'E': 0, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 0, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 1, 'A': 0},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 1, 'E': 1, 'J': 0, 'A': 0},
           {'M': 1, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 1, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 1, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 1, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 1, 'B': 0, 'E': 1, 'J': 1, 'A': 1},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 1, 'B': 0, 'E': 0, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 1, 'J': 0, 'A': 0},
           {'M': 0, 'B': 0, 'E': 0, 'J': 0, 'A': 0}]

    if observations is None:
        obs = _obs
    else:
        with open(observations, 'r') as f:
            obs = json.load(f)

    if n > len(obs):
        n = len(obs)
    _temp_obs = []
    for i in range(n):
        _temp_obs.append(obs[i])
    obs = _temp_obs
    print('using ' + str(len(obs)) + ' observations')

    vh = False
    for v in vals:
        if vals[v] == "x":
            vh = True
    nodes = [BetaNode('b_B', 1, 1, val=_get_value(vals, 'b_B', False), hyper=True, observed=_get_observed(vals, 'b_B', vh)),
             BetaNode('b_E', 1, 1, val=_get_value(vals, 'b_E', False), hyper=True, observed=_get_observed(vals, 'b_E', vh)),
             BetaNode('b_A_11', 1, 1, val=_get_value(vals, 'b_A_11', False), hyper=True, observed=_get_observed(vals, 'b_A_11', vh)),
             BetaNode('b_A_10', 1, 1, val=_get_value(vals, 'b_A_10', False), hyper=True, observed=_get_observed(vals, 'b_A_10', vh)),
             BetaNode('b_A_01', 1, 1, val=_get_value(vals, 'b_A_01', False), hyper=True, observed=_get_observed(vals, 'b_A_01', vh)),
             BetaNode('b_A_00', 1, 1, val=_get_value(vals, 'b_A_00', False), hyper=True, observed=_get_observed(vals, 'b_A_00', vh)),
             BetaNode('b_J_1', 1, 1, val=_get_value(vals, 'b_J_1', False), hyper=True, observed=_get_observed(vals, 'b_J_1', vh)),
             BetaNode('b_J_0', 1, 1, val=_get_value(vals, 'b_J_0', False), hyper=True, observed=_get_observed(vals, 'b_J_0', vh)),
             BetaNode('b_M_1', 1, 1, val=_get_value(vals, 'b_M_1', False), hyper=True, observed=_get_observed(vals, 'b_M_1', vh)),
             BetaNode('b_M_0', 1, 1, val=_get_value(vals, 'b_M_0', False), hyper=True, observed=_get_observed(vals, 'b_M_0', vh))]

    num_obs = [1 for x in nodes if x.observed]
    num_obs = sum(num_obs)
    print(num_obs, ' observed hyper-parameters')

    cdict = {'B': [], 'E': [], 'A': [], 'J': [], 'M': []}
    _cons = []

    for i, o in enumerate(obs):
        B = 'B'+str(i)
        E = 'E'+str(i)
        A = 'A'+str(i)
        J = 'J'+str(i)
        M = 'M'+str(i)
        nodes.append(BinaryNode(B, {(): 'b_B'}, val=_get_value(o,'B'), observed=_get_observed(o, 'B')))
        nodes.append(BinaryNode(E, {(): 'b_E'}, val=_get_value(o,'E'), observed=_get_observed(o, 'E')))
        nodes.append(BinaryNode(A, {(1, 1): 'b_A_11', (1, 0): 'b_A_10', (0, 1): 'b_A_01', (0, 0): 'b_A_00'}, val=_get_value(o,'A'), observed=_get_observed(o, 'A')))
        nodes.append(BinaryNode(J, {(1,): 'b_J_1', (0,): 'b_J_0'}, val=_get_value(o,'J'), observed=_get_observed(o, 'J')))
        nodes.append(BinaryNode(M, {(1,): 'b_M_1', (0,): 'b_M_0'}, val=_get_value(o,'M'), observed=_get_observed(o, 'M')))
        cdict['B'].append(B)
        cdict['E'].append(E)
        cdict['A'].append(A)
        cdict['J'].append(J)
        cdict['M'].append(M)
        _cons.append((B, [A]))
        _cons.append((E, [A]))
        _cons.append((A, [J, M]))

    if inference:
        nodes.append(BinaryNode('B', {(): 'b_B'}))
        nodes.append(BinaryNode('E', {(): 'b_E'}))
        nodes.append(BinaryNode('A', {(1, 1): 'b_A_11', (1, 0): 'b_A_10', (0, 1): 'b_A_01', (0, 0): 'b_A_00'}))
        nodes.append(BinaryNode('J', {(1,): 'b_J_1', (0,): 'b_J_0'}))
        nodes.append(BinaryNode('M', {(1,): 'b_M_1', (0,): 'b_M_0'}, val=1, observed=True))
        cdict['B'].append('B')
        cdict['E'].append('E')
        cdict['A'].append('A')
        cdict['J'].append('J')
        cdict['M'].append('M')
        _cons.append(('B', ['A']))
        _cons.append(('E', ['A']))
        _cons.append(('A', ['J', 'M']))

    _cons.append(('b_B', cdict['B']))
    _cons.append(('b_E', cdict['E']))
    _cons.append(('b_A_11', cdict['A']))
    _cons.append(('b_A_10', cdict['A']))
    _cons.append(('b_A_01', cdict['A']))
    _cons.append(('b_A_00', cdict['A']))
    _cons.append(('b_J_1', cdict['J']))
    _cons.append(('b_J_0', cdict['J']))
    _cons.append(('b_M_1', cdict['M']))
    _cons.append(('b_M_0', cdict['M']))

    connections = OrderedDict(_cons)

    return Graph(connections, nodes)


def _get_value(obs, letter, inv=True):
    x = obs[letter]
    if isinstance(x, str):
        if inv:
            return 0
        else:
            return 0.1
    else:
        return x


def _get_observed(obs, letter, inv=True):
    if inv:
        return obs[letter] != 'x'
    else:
        return False


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


def _eval_num_dict(n):
    if n == 0:
        return {'mu': [5., 1 / 9], 'sigma2': [11., 2.5]}
    elif n == 1:
        return {'mu': ['mu_mu', 1/9], 'sigma2': [11., 2.5]}
    elif n == 2:
        return {'mu': ['mu_mu', 'mu_var'], 'sigma2': [11., 2.5]}
    elif n == 3:
        return {'mu': ['mu_mu', 'mu_var'], 'sigma2': ["var_a", 2.5]}
    elif n == 4:
        return {'mu': ['mu_mu', 'mu_var'], 'sigma2': ["var_a", "var_b"]}


def _eval_connect_dict(n):
    if n == 0:
        return {}
    elif n == 1:
        return {'mu_mu': ['mu']}
    elif n == 2:
        return {'mu_mu': ['mu'], 'mu_var': ['mu']}
    elif n == 3:
        return {'mu_mu': ['mu'], 'mu_var': ['mu'], 'var_a': ['sigma2']}
    elif n == 4:
        return {'mu_mu': ['mu'], 'mu_var': ['mu'], 'var_a': ['sigma2'], 'var_b': ['sigma2']}


def faculty_evals_1hyper(n):
    scores = [6.39, 6.32, 6.25, 6.24, 6.21, 6.18, 6.17, 6.13, 6.00, 6.00, 5.97, 5.82, 5.81, 5.71, 5.55, 5.50, 5.39,
              5.37, 5.35, 5.30, 5.27, 4.94, 4.50]

    hyper_nodes = [NormalNode('mu_mu', 5.7, 1, val=5.7),
                   InverseGammaNode('mu_var', 3, .3, val=1/9),
                   GammaNode('var_a', 30, 2.75, val=11.),
                   GammaNode('var_b', 5, 1.3)]

    plate_nodes = [NormalNode('x' + str(i), 'mu', 'sigma2', val=score, observed=True) for i, score in enumerate(scores)]
    hyper_params = _eval_num_dict(n)

    nodes = [hyper_nodes[i] for i in range(n)]

    nodes += [NormalNode('mu', hyper_params['mu'][0], hyper_params['mu'][1], cand_var=0.2, val=5.),
              InverseGammaNode('sigma2', hyper_params['sigma2'][0], hyper_params['sigma2'][1], cand_var=0.15, val=0.3)]

    nodes += plate_nodes

    connections = _eval_connect_dict(n)
    connections['mu'] = ['x' + str(i) for i in range(len(scores))]
    connections['sigma2'] = ['x' + str(i) for i in range(len(scores))]

    return Graph(connections, nodes)


def tanks():
    n = 1556
    num_obs = 200
    obs_tanks = [random.randint(0, n) for x in range(num_obs)]

    def f(a):
        return a._val * 10

    # obs_tanks = [46, 22, 101, 6, 94, 116, 28, 32, 37, 12, 10, 54, 93, 94, 50, 15, 29, 38, 89, 86]
    nodes = [GammaNode('A', 1, 2),
        ParetoNode('num_tanks', Param(f, 'A'), 200, val=200, cand_var=2000)]
    for i, tank in enumerate(obs_tanks):
        nodes.append(UniformNode(str(i), 'num_tanks', val=tank, observed=True))
    connections = {'A': ['num_tanks'],
                   'num_tanks': [str(i) for i in range(num_obs)]}
    return Graph(connections, nodes)


def wacky_b(a):
    return a._val ** math.pi


def wacky():
    nodes = [NormalNode('A', 20.,1., val=20, cand_var=15),
             BetaNode('E', 1, 1, val=0.5, cand_var=1/8),
             GammaNode('B', Param(wacky_b, 'A'), 7, val=1700, cand_var=700**2),
             BetaNode('D', 'A', 'E', val=0.5, cand_var=1/8),
             BinaryNode('C', BernoulliParam()),
             PoissonNode('F', 'D', cand_var=1.5),
             NormalNode('G', 'E', 'F', val=5)]
    connections = OrderedDict([('A', ['B', 'D']),
                               ('E', ['D', 'G']),
                               ('D', ['C', 'F']),
                               ('F', ['G'])])
    return Graph(connections, nodes)


def golf():
    golfers = {}
    tournaments = {}
    tour_connects = {}
    observations = []
    with open('golfers.csv', newline='') as golf_data:
        reader = csv.reader(golf_data, delimiter=' ')
        for i,line in enumerate(reader):
            golfer = line[0]
            score = float(line[1])
            tour = 't' + line[2]
            name = 'obs' + str(i)

            golfers[golfer] = golfers.setdefault(golfer, [])+[name]
            tournaments[tour] = tournaments.setdefault(tour, [])+[name]
            tour_connects[(tour, golfer)] = name
            observations.append((name, score, golfer, tour))
    print('read in golf data')

    nodes = [NormalNode('hypertour-mean', 72, 2, val=72.8, cand_var=2),
             InverseGammaNode('hypertour-var', 18, 1/0.015, val=3),
             InverseGammaNode('hypergolfer-var', 18, 1/0.015, val=3.5),
             InverseGammaNode('obsvar', 83, 1/0.0014, val=3.1)]
    for tour in tournaments:
        nodes.append(NormalNode(tour, 'hypertour-mean', 'hypertour-var', val=72))
    print('created tournament nodes')
    for golfer in golfers:
        nodes.append(NormalNode(golfer, 0, 'hypergolfer-var', val=0))
    print('created golfer nodes')
    for obs in observations:
        name = obs[0]
        score = obs[1]
        golfer = obs[2]
        tour = obs[3]
        f = lambda g, t: g._val + t._val
        nodes.append(NormalNode(name, Param(f, golfer, tour), 'obsvar', val=score, observed=True))
    print('created observation nodes')
    connections = {'hypertour-mean': [t for t in tournaments],
                   'hypertour-var': [t for t in tournaments],
                   'hypergolfer-var': [g for g in golfers]}
    print('added hyper connections')
    for tour, obs in tournaments.items():
        connections[tour] = obs
    print('added tour connections')
    for golfer, obs in golfers.items():
        connections[golfer] = obs
    print('added golfer connections')
    connections['obsvar'] = [obs[0] for obs in observations]
    print('added observation-variance connections')
    result = Graph(connections, nodes)
    result.golfers = golfers
    print('created graph')
    return result


def beta_bernoulli(b=1):
    nodes = [BetaNode('A', 2., 3.),
             BinaryNode('B', BernoulliParam(), val=b, observed=True)]
    connections = OrderedDict([('A', ['B'])])
    return Graph(connections, nodes)



def normal_normal():
    mu = lambda a: a._val + 2
    nodes = [NormalNode('A', 0., 1.),
             NormalNode('B', Param(mu, 'A'), 1., val=1.2, observed=True)]
    connections = OrderedDict([('A', ['B'])])
    return Graph(connections, nodes)


def gamma_poisson():
    nodes = [GammaNode('L', 2., 3.),
             PoissonNode('X', 'L', val=3, observed=True)]
    connections = OrderedDict([('L', ['X'])])
    return Graph(connections, nodes)


def bernoulli_simple():
    nodes = [BernoulliNode('B', 0.1)]
    connections = OrderedDict([])
    return Graph(connections, nodes)


def progress():
    def r(a):
        return 1. / a._val

    nodes = [BetaNode('Progress', 2., 15.),
             PoissonNode('Encounters', Param(r, 'Progress'))]
    connections = OrderedDict([('Progress', ['Encounters'])])
    return Graph(connections, nodes)


def pareto():
    nodes = [GammaNode('A', 9., 2.),
             ParetoNode('Lambda', 'A', 22, val=22, cand_var=3),
             PoissonNode('C', 'Lambda', val=23)]
    connections = {'A': ['Lambda'], 'Lambda': ['C']}
    return Graph(connections, nodes)
