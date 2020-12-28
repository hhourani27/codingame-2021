import numpy as np
from collections import deque
from test_cases import test_cases

#%% Game Input
test_case = test_cases[4]
v,e,g,graph,gws,si =[k[1] for k in test_case.items()]

#%% Game init
PLAYER,AGENT = (0,1)
gw_links = set()
for gw in gws:
    gwps = graph[gw].nonzero()[0]
    for gwp in gwps:
        gw_links.add((gwp,gw))
        
node_counter = 0

#%% Minimax setup
# State = (action,player,graph,gw_links,agentPos)
# Action = gw to cut

def terminal(state):
    if len(state[3]) == 0: return True
    if state[4] in gws : return True
    
def utility(state):
    if len(state[3]) == 0: return 1
    if state[4] in gws : return -1
    
def shortest_path(graph,start,goal):
    frontier = deque([start])
    parent = {start:None}
    
    found_goal = False
    while len(frontier) > 0:
        current = frontier.popleft()
        if current == goal:
            found_goal = True
            break
        neighbors = graph[current].nonzero()[0]
        for neighbor in neighbors:
            if neighbor not in parent:
                frontier.append(neighbor)
                parent[neighbor] = current
                
    if found_goal is True:
        while True:
            prev_node = parent[current]
            if prev_node == start: return current
            current = prev_node
    else:
        return None

def successors(state) :
    action,player,graph,gw_links,agentPos = state
    successors = []
    if player == PLAYER:
        for gwl in gw_links:
            gwp,gw = gwl
            
            next_graph = graph.copy()
            next_graph[gwp][gw] = False
            next_graph[gw][gwp] = False

            next_gw_links = gw_links.copy()
            next_gw_links.remove(gwl)            
            successors.append((gwl,AGENT,next_graph,next_gw_links,agentPos))

    elif player == AGENT:
        gwps = {gwp for gwp,gw in gw_links}
        if agentPos in gwps:
            neighbors = graph[agentPos].nonzero()[0]
            for n in neighbors:
                if n in gws:
                    successors.append((n,PLAYER,graph,gw_links,n))
        else:
            closest_nodes = {shortest_path(graph, agentPos, gwp) for gwp in gwps}
            for n in closest_nodes:
                successors.append((n,PLAYER,graph,gw_links,n))
    
#    print('{} -> {}'.format(state,successors))
    return successors
    
def max_value(state,alpha,beta) : 
    global node_counter
    node_counter += 1
    
    if terminal(state):
        return (utility(state),state[0])
    v = -10
    best_action = None
    for s in successors(state):
        v2,a = min_value(s,alpha,beta)
        if v2 > v:
            v = v2
            best_action = s[0]
        if v >= beta: return (v,best_action)
        alpha = max(alpha,v)
    return (v,best_action)

def min_value(state,alpha,beta) :
    global node_counter
    node_counter += 1
    
    if terminal(state):
        return (utility(state),state[0])
    v = 10
    best_action = None
    for s in successors(state):
        v2,a = max_value(s,alpha,beta)
        if v2 < v:
            v = v2
            best_action = s[0]
        if v <= alpha: return (v,best_action)
        beta = min(beta,v)
    return (v,best_action)


def minimax(state):
    v,a = max_value(state,-10,10)
    return a
    
#%% Turn input

# Play
init_state = (None,PLAYER,graph,gw_links,si)
action = minimax(init_state)