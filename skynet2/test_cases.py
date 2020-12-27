# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 20:05:54 2020

@author: hhour
"""
import numpy as np

test_cases = {
# Test case 1 : Robust double gateways
# Game tree :2093 nodes
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
# Game tree :2273 nodes
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
# Game tree : nodes
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