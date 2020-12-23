# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 16:34:11 2020

@author: hhour
"""
import time
from collections import deque


RIGHT,LEFT = (0,1)
WAIT,BLOCK,ELEVATOR = (0,1,2)

test_cases = {
#Test 01 : 
# -803- -115- -108- 32 nodes in game tree
1:{'nb_floors' : 2,
'width' : 13,
'nb_rounds' : 100,
'exit_floor' : 1,
'exit_pos' : 11,
'nb_total_clones' : 10,
'nb_add_elevators' : 1,
'nb_elevators' :  0,
'elevators' : (),
'start_floor' : 0,
'start_pos' : 2,
},
#Test 02 : Elevator: U Turn
# -763- -105- -100- 31 nodes in game tree
2:{'nb_floors' : 2,
'width' : 13,
'nb_rounds' : 100,
'exit_floor' : 1,
'exit_pos' : 2,
'nb_total_clones' : 10,
'nb_add_elevators' : 1,
'nb_elevators' :  0,
'elevators' : (),
'start_floor' : 0,
'start_pos' : 9,
},
#Test 03 : One elevator per floor
# -1565- -1491- 87 nodes in game tree 
3:{'nb_floors' : 6,
'width' : 13,
'nb_rounds' : 100,
'exit_floor' : 5,
'exit_pos' : 10,
'nb_total_clones' : 10,
'nb_add_elevators' : 5,
'nb_elevators' :  0,
'elevators' : (),
'start_floor' : 0,
'start_pos' : 1,
},
#Test 04 : 2 Missing 'elevators'
# -1306- -1281- -1193- -150- 99 nodes in game tree 
4:{'nb_floors' : 6,
'width' : 13,
'nb_rounds' : 100,
'exit_floor' : 5,
'exit_pos' : 1,
'nb_total_clones' : 10,
'nb_add_elevators' : 2,
'nb_elevators' :  3,
'elevators' : ((4, 1), (0, 4), (2, 7)),
'start_floor' : 0,
'start_pos' : 10,
},
#Test 05 : 3 Missing 'elevators'
# -805- -769- -737- -163- 109 nodes in game tree 
5:{'nb_floors' : 7,
'width' : 13,
'nb_rounds' : 30,
'exit_floor' : 6,
'exit_pos' : 7,
'nb_total_clones' : 10,
'nb_add_elevators' : 3,
'nb_elevators' :  3,
'elevators' : ((3, 7), (0, 6), (2, 6)),
'start_floor' : 0,
'start_pos' : 4,
},
#Test 06 : Best path
# -433- 412 nodes in game tree 
6:{'nb_floors' : 10,
'width' : 19,
'nb_rounds' : 47,
'exit_floor' : 9,
'exit_pos' : 9,
'nb_total_clones' : 41,
'nb_add_elevators' : 0,
'nb_elevators' :  17,
'elevators' : ((3, 4), (4, 3), (7, 4), (1, 17), (8, 9), (4, 9), (2, 3), (0, 3), (5, 4), (7, 17), (1, 4), (3, 17), (2, 9), (6, 9), (5, 17), (0, 9), (6, 3)),
'start_floor' : 0,
'start_pos' : 6,
},
#Test 07 : Missing elevator
# -1729- -1600- -810- 684 nodes in game tree 
7:{'nb_floors' : 10,
'width' : 19,
'nb_rounds' : 42,
'exit_floor' : 9,
'exit_pos' : 9,
'nb_total_clones' : 41,
'nb_add_elevators' : 1,
'nb_elevators' :  16,
'elevators' : ((4, 3), (7, 4), (1, 17), (8, 9), (4, 9), (2, 3), (0, 3), (5, 4), (7, 17), (1, 4), (3, 17), (2, 9), (6, 9), (5, 17), (0, 9), (6, 3)),
'start_floor' : 0,
'start_pos' : 6,
},
#Test 08 : Trap
# 2554 nodes in game tree 
8:{'nb_floors' : 13,
'width' : 36,
'nb_rounds' : 67,
'exit_floor' : 11,
'exit_pos' : 12,
'nb_total_clones' : 41,
'nb_add_elevators' : 4,
'nb_elevators' :  34,
'elevators' : ((6, 34), (2, 23), (10, 3), (7, 34), (5, 4), (10, 23), (1, 24), (11, 11), (10, 34), (8, 23), (6, 13), (6, 22), (11, 4), (9, 2), (4, 9), (0, 34), (2, 34), (3, 17), (4, 23), (4, 34), (1, 17), (1, 4), (9, 17), (5, 34), (2, 3), (8, 9), (8, 1), (7, 17), (9, 34), (1, 34), (2, 24), (3, 34), (11, 13), (8, 34)),
'start_floor' : 0,
'start_pos' : 6,
},
#Test 09 : Few clones
#  nodes in game tree 
9:{'nb_floors' : 13,
'width' : 69,
'nb_rounds' : 79,
'exit_floor' : 11,
'exit_pos' : 39,
'nb_total_clones' : 8,
'nb_add_elevators' : 5,
'nb_elevators' :  30,
'elevators' : ((6, 65), (11, 4), (8, 34), (8, 56), (7, 17), (8, 1), (2, 24), (11, 13), (10, 23), (6, 13), (6, 34), (5, 4), (1, 50), (5, 46), (3, 17), (10, 3), (11, 42), (1, 17), (1, 4), (2, 23), (8, 66), (2, 3), (1, 24), (1, 34), (8, 9), (2, 58), (11, 11), (11, 38), (8, 23), (6, 57)),
'start_floor' : 0,
'start_pos' : 33,
},
#Test 10 : Giant map
#  nodes in game tree 
10:{'nb_floors' : 13,
'width' : 69,
'nb_rounds' : 109,
'exit_floor' : 11,
'exit_pos' : 47,
'nb_total_clones' : 100,
'nb_add_elevators' : 4,
'nb_elevators' :  36,
'elevators' : ((2, 56), (4, 23), (8, 1), (3, 30), (4, 9), (9, 17), (11, 45), (6, 9), (1, 24), (7, 48), (3, 24), (8, 63), (10, 45), (9, 2), (2, 23), (3, 17), (10, 3), (1, 36), (2, 9), (10, 23), (1, 62), (1, 17), (1, 4), (8, 23), (2, 43), (2, 3), (6, 3), (6, 23), (5, 4), (6, 35), (11, 4), (11, 50), (8, 9), (1, 50), (2, 24), (3, 60)),
'start_floor' : 0,
'start_pos' : 6,
}
}

def printActions(end_node, parent) :
    actions = []
    current = end_node
    while current is not None:
        print(current)
        
        action = current[6]
        if action == WAIT:
            actions = [action] + actions
        elif action == BLOCK:
            actions = [action,WAIT,WAIT] + actions
        elif action == ELEVATOR:
            actions = [action,WAIT,WAIT,WAIT] + actions
    
        current = parent[current]

    print(actions)


#%%

test_case = test_cases[8]
nb_floors,width,nb_rounds,exit_floor,exit_pos,nb_total_clones,nb_add_elevators,nb_elevators,elevators,start_floor,start_pos=[k[1] for k in test_case.items()]


#Node
#(f,y,direction,round,elevators,clones_left,add_elevators_left,action_for_next_round)

allowed_y_elevators = dict()
allowed_y_elevators[0] = set()
for i in range(1,exit_floor-1):
    allowed_y_elevators[i] = set()
    for e in elevators + ((0,start_pos),):
        if e[0] == i-1:
                allowed_y_elevators[i].add(e[1])
allowed_y_elevators[exit_floor-1] = {exit_pos}

for i in range(1,exit_floor):
    if len(allowed_y_elevators[i]) == 0:
        allowed_y_elevators[i] = allowed_y_elevators[i-1]
    

start_state = (start_floor,start_pos,RIGHT,1,nb_total_clones,nb_add_elevators)
start_WAIT = start_state + (WAIT,)
start_BLOCK = start_state + (BLOCK,)


frontier = deque([
    start_WAIT,
    start_BLOCK
            ])
parent = {
    start_WAIT: None,
    start_BLOCK: None
    }

if nb_add_elevators > 0:
    start_ELEVATOR = start_state + (ELEVATOR,)
    frontier.append(start_ELEVATOR)
    parent[start_ELEVATOR] = None

loop = 0
start_time = time.time()
while len(frontier) > 0:
    if loop % 100000 == 0:
        loop_duration = time.time() - start_time
        print('Loop: {}, tree: {}, frontier: {}, {:.1f} s'
              .format(loop,len(parent),len(frontier),loop_duration))
        start_time = time.time()
    loop += 1
    
    current  = frontier.popleft()
    f,y,dir,round,clones_left,add_elevator_left,action = current
    next_f,next_y,next_dir,next_round,next_clones_left,next_add_elevator_left,next_action = current

    
    # check if I arrived to goal
    if f == exit_floor and y == exit_pos: 
        break
    
    
    # apply action and prepare state for next round
    if action == WAIT:
        if (f,y) in elevators:
            next_f  = f + 1
        else:
            next_y = y+1 if dir == RIGHT else y-1
        next_round = round + 1
    elif action == BLOCK:
        next_dir = RIGHT if dir == LEFT else LEFT
        next_clones_left = clones_left - 1
        next_round = round + 3
    elif action == ELEVATOR:
        next_f = f + 1
        next_add_elevator_left = add_elevator_left - 1
        next_clones_left = clones_left - 1
        next_round = round + 4
        
    # check if next state is a lost one
    if next_y < 0 or next_y >= width:
        continue
    elif next_round > nb_rounds:
        continue
    elif next_f > exit_floor:
        continue
    elif next_clones_left <= 0:
        continue
        # check if there's no more add elevators and there's floors with no elevators
    
    next_state = (next_f,next_y,next_dir,next_round,next_clones_left,next_add_elevator_left)
    # decide on possible actions
    next_WAIT = next_state + (WAIT,)
    frontier.append(next_WAIT)
    parent[next_WAIT] = current

    # Only block at the exit of elevators
    if next_clones_left > 0:
        if next_f > f and (next_f,next_y) not in elevators:
            next_BLOCK = next_state + (BLOCK,)
            frontier.append(next_BLOCK)
            parent[next_BLOCK] = current
    
    if next_clones_left > 0 and next_add_elevator_left > 0 and next_f < exit_floor:
        if (next_f,next_y) not in elevators : #don't add an elevator on an existing elevator
            if next_y in allowed_y_elevators[next_f] :  #only add elevators under an existing elevator or under exit
                next_ELEVATOR = next_state + (ELEVATOR,)
                frontier.append(next_ELEVATOR)
                parent[next_ELEVATOR] = current


printActions(current, parent)

#%%
'''
for after,before in parent.items():
    if before == (0, 33, 0, 1, 5, 2):
        print(after)
'''
frontier = list(frontier)
f1 = list(filter(lambda x :x[0] == 0 and x[6] == BLOCK,frontier))
f2 = sorted(f1, key = lambda x : (x[0],x[1]))	