
from graph import Graph
from graph import Node


def alarm():
    nodes = [Node('B', {(): 0.001}),
             Node('E', {(): 0.002}),
             Node('A', {(1, 1): 0.95, (1, 0): 0.94, (0, 1): 0.29, (0, 0): 0.001}),
             Node('J', {(1,): 0.9, (0,): 0.05}, observed=True),
             Node('M', {(1,): 0.7, (0,): 0.01}, observed=True)]
    connections = {'B': ['A'],
                   'E': ['A'],
                   'A': ['J', 'M']}
    return Graph(connections, nodes)
