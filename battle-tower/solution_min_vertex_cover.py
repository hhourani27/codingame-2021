from collections import deque
from test_cases import test_cases

# see https://www.cl.cam.ac.uk/teaching/1415/AdvAlgo/lec8_ann.pdf

TC = test_cases[6]

input = iter(TC.splitlines())

n = int(next(input))
graph = dict()
for i in range(n):
    line = next(input).split()
    node = int(line[0])
    neighbors = [int(v) for v in line[2:]]
    graph[node] = neighbors

if n == 1:
    print(1)
else:
    # create tree with root 1
    tree = dict()
    reverse_tree = dict()
    visited = set()
    node = 1
    frontier = deque([1])
    while len(frontier) > 0:
        curr = frontier.popleft()
        visited.add(curr)
        neighbors = graph[curr]
        unvisited_neighbors = [v for v in neighbors if v not in visited]
        tree[curr] = unvisited_neighbors
        for u in unvisited_neighbors:
            reverse_tree[u] = curr
        
        frontier.extend(unvisited_neighbors)
        
    # min vertex cover of tree
    cover = set()
    tree_t = {v:[c for c in ch] for v,ch in tree.items()}
    reverse_tree_t = reverse_tree.copy()
    while len(tree_t) > 0:
        # get all leaves
        leaves = [v for v in tree_t.keys() if len(tree_t[v]) == 0]
        # get parents of all leaves and 
        parents = set()
        cover_new = set()
        for v in leaves:
            if v in reverse_tree_t:
                parents.add(reverse_tree_t[v])
                cover.add(reverse_tree_t[v])
                cover_new.add(reverse_tree_t[v])
            else:
                cover_new.add(v)
        # add parents to cover
        # delete all leaves
        for v in leaves:
            del tree_t[v]
            if v in reverse_tree_t:
                del reverse_tree_t[v]
        # delete all parents
        for p in cover_new:
            if p in tree_t:
                del tree_t[p]
            if p in reverse_tree_t:
                del reverse_tree_t[p]
        for p in cover_new:
            for v in tree_t.values():
                if p in v:
                    v.remove(p)
    print(len(cover))

#%% Draw tree
dot = 'graph G { \n'
for v in range(1,n+1):
    if v in cover:
        dot += '{} [color=red,style=filled];\n'.format(v)
    for c in tree[v]:
        dot += '{} -- {};\n'.format(v,c)
dot += '}'

#%%
covered = set()
taken = set()
def mvc(v):
    for c in tree[v]:
        mvc(c)
    if v not in covered:
        if v in reverse_tree:
            parent = reverse_tree[v]
            taken.add(parent)
            covered.update(tree[parent])
            covered.add(reverse_tree[parent])
            covered.add(parent)
        else:
            taken.add(v)
            covered.update(tree[v])
            covered.add(v)
        a = 1
    else:
        pass
            
mvc(1)