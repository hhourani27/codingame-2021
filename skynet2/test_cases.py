# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 20:05:54 2020

@author: hhour
"""
import numpy as np
import math

# gwl = gw links
# avb = average # edges for each node
# Approximate # nodes in game tree = avb^gwl * gwl!

test_cases = {
# Test case 1 : Robust double gateways
# expected game tree size: 2678
# Game tree : -2093- -179- -287- -75- 146 nodes
# Solution : (3,4)
1: {
    'v': 8,
    'e': 13,
    'g': 2,
    'graph': np.array([[False,  True,  True,  True, False, False, False, False],
                       [ True, False, False,  True, False, False, False,  True],
                       [ True, False, False,  True, False, False,  True, False],
                       [ True,  True,  True, False,  True,  True,  True,  True],
                       [False, False, False,  True, False, False, False,  True],
                       [False, False, False,  True, False, False,  True, False],
                       [False, False,  True,  True, False,  True, False, False],
                       [False,  True, False,  True,  True, False, False, False]]),
    'gws': {4,5},
    'si': 0
    },
# Test case 2 : Linked double gateways
# expected game tree size: 1475
# Game tree :-2273- -477- -277- -105- 107 nodes
# Solution (2,5) or (2,6)
2: {
    'v': 10,
    'e': 14,
    'g': 4,
    'graph': np.array([[False, False, False, False, False, False, False,  True,  True,True],
                       [False, False,  True,  True,  True, False, False,  True, False,True],
                       [False,  True, False, False, False,  True,  True, False,  True,True],
                       [False,  True, False, False, False, False, False, False, False,False],
                       [False,  True, False, False, False, False, False, False, False,False],
                       [False, False,  True, False, False, False, False, False, False,False],
                       [False, False,  True, False, False, False, False, False, False,False],
                       [ True,  True, False, False, False, False, False, False, False,True],
                       [ True, False,  True, False, False, False, False, False, False,True],
                       [ True,  True,  True, False, False, False, False,  True,  True,False]]),
    'gws': {3, 4, 5, 6},
    'si': 0
    },
# Test case 3 : Leading up to a double gateway
# expected game tree size: 614M
# Game tree : -61297- -23221- 1753 nodes
# Solution (9,0)
3: {
    'v': 12,
    'e': 20,
    'g': 2,
    'graph': np.array([[False,  True,  True,  True,  True,  True,  True, False, False,True, False, False],
                       [ True, False,  True, False, False, False,  True, False, False,False, False, False],
                       [ True,  True, False,  True, False, False, False, False, False,False, False, False],
                       [ True, False,  True, False,  True, False, False, False, False,False, False, False],
                       [ True, False, False,  True, False,  True, False, False, False,False, False, False],
                       [ True, False, False, False,  True, False, False, False, False,True, False,  True],
                       [ True,  True, False, False, False, False, False,  True, False,False, False, False],
                       [False, False, False, False, False, False,  True, False, False,False, False, False],
                       [False, False, False, False, False, False, False, False, False,True,  True, False],
                       [ True, False, False, False, False,  True, False, False,  True,False,  True,  True],
                       [False, False, False, False, False, False, False, False,  True,True, False,  True],
                       [False, False, False, False, False,  True, False, False, False,True,  True, False]]),
    'gws': {0, 7},
    'si': 8
    },
# Test case 4 : Ordered gateways
# expected game tree size: 660M
# Game tree : -25294- 13192 nodes
# Solution (1,12)
4: {
    'v': 22,
    'e': 37,
    'g': 7,
    'graph': np.array([[False,  True,  True,  True,  True,  True, False, False, False,False, False, False, False, False, False, False, False, False,False, False, False, False],
       [ True, False,  True, False, False,  True, False, False,  True,False, False, False,  True, False, False,  True, False, False,False, False, False, False],
       [ True,  True, False,  True, False, False, False, False,  True,True, False, False, False, False, False, False, False, False,False, False, False, False],
       [ True, False,  True, False,  True, False, False, False, False,True,  True, False, False, False, False, False, False, False,False, False, False,  True],
       [ True, False, False,  True, False,  True, False, False, False,False,  True, False, False, False,  True, False, False, False,False, False, False, False],
       [ True,  True, False, False,  True, False, False,  True, False,False, False, False, False,  True, False, False, False, False,False, False, False, False],
       [False, False, False, False, False, False, False, False, False,False,  True,  True, False,  True,  True, False,  True,  True,False, False, False, False],
       [False, False, False, False, False,  True, False, False,  True,False, False, False,  True, False, False, False, False,  True,False, False,  True, False],
       [False,  True,  True, False, False, False, False,  True, False,True, False, False, False, False, False, False, False, False,False, False, False, False],
       [False, False,  True,  True, False, False, False, False,  True,False, False, False, False, False, False, False, False, False,False,  True, False,  True],
       [False, False, False,  True,  True, False,  True, False, False,False, False, False, False, False, False, False, False, False,True, False, False,  True],
       [False, False, False, False, False, False,  True, False, False,False, False, False, False, False, False, False, False, False,False, False, False, False],
       [False,  True, False, False, False, False, False,  True, False,False, False, False, False, False, False, False, False, False,False, False, False, False],
       [False, False, False, False, False,  True,  True, False, False,False, False, False, False, False, False, False, False, False,False, False, False, False],
       [False, False, False, False,  True, False,  True, False, False,False, False, False, False, False, False, False, False, False,False, False, False, False],
       [False,  True, False, False, False, False, False, False, False,False, False, False, False, False, False, False, False, False,False, False, False, False],
       [False, False, False, False, False, False,  True, False, False,False, False, False, False, False, False, False, False, False,False, False, False, False],
       [False, False, False, False, False, False,  True,  True, False,False, False, False, False, False, False, False, False, False,False, False, False, False],
       [False, False, False, False, False, False, False, False, False,False,  True, False, False, False, False, False, False, False,False, False, False, False],
       [False, False, False, False, False, False, False, False, False,True, False, False, False, False, False, False, False, False,False, False, False, False],
       [False, False, False, False, False, False, False,  True, False,False, False, False, False, False, False, False, False, False,False, False, False, False],
       [False, False, False,  True, False, False, False, False, False,True,  True, False, False, False, False, False, False, False,False, False, False, False]]),
    'gws': {11, 12, 15, 16, 18, 19, 20},
    'si': 0
    },
# Test case 5 : Complex mesh
# expected game tree size: 1.6E31
# Game tree :  nodes
# Solution 
5: {
    'v': 37,
    'e': 81,
    'g': 4,
    'graph': np.array([[0,1,0,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0],
                        [0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                        [0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                        [1,1,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [1,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                        [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,1,0,1,1,1,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                        [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                        [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0],
                        [0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                        [0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]),
    'gws': {0, 16, 18, 26},
    'si': 2
    },

}


#%%
def estimate_tree_size(n):
    test_case = test_cases[n]
    v,e,g,graph,gws,si =[k[1] for k in test_case.items()]
    
    gwl = 0
    for gw in gws:
        neighbors = graph[gw].nonzero()[0]
        gwl += len(neighbors)
    
    neighbors = [len(graph[n].nonzero()[0]) for n in range(v)]
    avb = sum(neighbors)/len(neighbors)
    
    tree_size = avb**gwl * math.factorial(gwl)
    
    return tree_size

#s = estimate_tree_size(5)
#print(s)