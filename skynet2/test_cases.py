# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 20:05:54 2020

@author: hhour
"""
import numpy as np

# gwl = gw links
# avb = average # edges for each node
# Approximate # nodes in game tree = avb^gwl * gwl!

test_cases = {
# Test case 1 : Robust double gateways
# expected game tree size: 2678
# Game tree : -2093- -179- 287 nodes
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
# Game tree :-2273- -477- 277 nodes
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
# Game tree : 61297 nodes
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

}