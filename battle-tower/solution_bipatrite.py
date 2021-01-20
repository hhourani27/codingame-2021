import numpy as np
import math
from collections import deque
from test_cases import test_cases

TC = test_cases[5]

input = iter(TC.splitlines())

n = int(next(input))
graph = dict()
for i in range(n):
    line = next(input).split()
    graph[line[0]] = line[2:]
    
# Return a 2-coloring of the graph
red = set()
blue = set()

cells = list(graph.keys())
red.add(cells[0])

frontier = deque([cells[0]])

while len(frontier) > 0:
    curr = frontier.popleft()
    neighbors = graph[curr]
    for v in neighbors:
        if v not in red and v not in blue:
            if curr in red:
                blue.add(v)
            else:
                red.add(v)
            frontier.append(v)
            
for v1 in graph.keys():
    for v2 in graph[v1]:
        if (v1 in red and v2 in red) or (v1 in blue and v2 in blue):
            print('NOT BIPARTITE')

if len(graph) == 1:
    print(1)
else:
    print(min(len(red),len(blue)))