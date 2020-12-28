# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 19:04:23 2020

@author: hhour
"""
import numpy as np
from test_cases import test_cases
import math

test_case = test_cases[3]
v,e,g,graph,gws,si =[k[1] for k in test_case.items()]

gwl = 0
for gw in gws:
    neighbors = graph[gw].nonzero()[0]
    gwl += len(neighbors)

neighbors = [len(graph[n].nonzero()[0]) for n in range(v)]
avb = sum(neighbors)/len(neighbors)

tree_size = avb**gwl * math.factorial(gwl)