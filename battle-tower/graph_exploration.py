from test_cases import test_cases
import networkx as nx
from networkx.algorithms import bipartite
from networkx.algorithms.approximation.vertex_cover import min_weighted_vertex_cover
from networkx.drawing.nx_agraph import graphviz_layout

TC = test_cases[5]

input = iter(TC.splitlines())

n = int(next(input))

#%% Create undirected graph

graph = nx.Graph()
graph.add_nodes_from(list(range(1,n+1)))

for i in range(n):
    line = next(input).split()
    node = int(line[0])
    neighbors = [int(v) for v in line[2:] if int(v) > node]
    for nb in neighbors:
        graph.add_edge(node,nb)

#%% Create directed graph
graph = nx.DiGraph()
graph.add_nodes_from(list(range(1,n+1)))

for i in range(n):
    line = next(input).split()
    node = int(line[0])
    neighbors = [int(v) for v in line[2:]]
    for nb in neighbors:
        graph.add_edge(node,nb)

#%% Analyse graph bipatrite
is_bipatrite = bipartite.is_bipartite(graph)
print('Is Bipatrite: {}'.format(is_bipatrite))
red = bipartite.sets(graph)[0]
blue = bipartite.sets(graph)[1]

print('Red nodes ({}): {}'.format(len(red),red))
print('Blue nodes ({}): {}'.format(len(blue),blue))

nx.draw(graph, with_labels=True)
#nx.draw(graph, with_labels=True, pos=nx.bipartite_layout(graph,red))
#nx.draw(graph, with_labels=True, pos=nx.circular_layout(graph))

#%% Analyze minimum vertex cover
min_vertex_cover = min_weighted_vertex_cover(graph)
print('Min vertex cover ({}): {}'.format(len(min_vertex_cover),min_vertex_cover))

#%% Analyze maximum matching
max_matching = bipartite.maximum_matching(graph)
print('Maximum matching ({}): {}'.format(len(max_matching),max_matching))

#%% Draw graph
nx.draw(graph, with_labels=True, pos=graphviz_layout(graph, prog='dot'))


