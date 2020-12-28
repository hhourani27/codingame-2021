import numpy as np
from collections import deque
from test_cases import test_cases
import time

#%% Game Input
test_case = test_cases[5]
v,e,g,graph,gws,si =[k[1] for k in test_case.items()]

#%% Game init
PLAYER,AGENT = (0,1)
gw_links = set()
for gw in gws:
    gwps = graph[gw].nonzero()[0]
    for gwp in gwps:
        gw_links.add((gwp,gw))

shortest_path_cache = dict()

node_counter = 0

#%% Minimax setup
# State = (action,player,graph,gw_links,agentPos)
# Action = gw to cut

def get_gwps(gw_links):
    return {gwp for gwp,gw in gw_links}

def links_to_gw(gw_links, gwp):
    count = 0
    for a,b in gw_links:
        if a == gwp:
            count += 1
    return count

def terminal(state):
    action,player,graph,gw_links,agentPos = state
    if len(gw_links) == 0: return 1
    if agentPos in gws : return -1
    if agentPos in get_gwps(gw_links) and links_to_gw(gw_links,agentPos) > 1: return -1
    
    return None
    
def shortest_path(graph,start,goal):
    #verify cache
    key = (start,goal)
    if key in shortest_path_cache:
        return shortest_path_cache[key]
    
    frontier = deque([start])
    parent = {start:None}
    
    while len(frontier) > 0:
        current = frontier.popleft()
        if current == goal:
            break
        neighbors = graph[current].nonzero()[0]
        for neighbor in neighbors:
            if neighbor not in parent:
                frontier.append(neighbor)
                parent[neighbor] = current
                
    distance = 1
        while True:
            prev_node = parent[current]
            if prev_node == start:
            shortest_path_cache[key] = (current,distance)
            return (current,distance)
            current = prev_node
        distance += 1
        if current is None:
            pass
        

    else:
        return None

def successors(state) :
    action,player,graph,gw_links,agentPos = state
    gwps = get_gwps(gw_links)
    
    successors = []
    if player == PLAYER:
        # if agent is on a gwp, choose the link to the gw
        if agentPos in gwps:
            gwl = list(filter(lambda x: x[0]==agentPos,gw_links))[0]
            gwp,gw = gwl
            next_graph = graph.copy()
            next_graph[gwp][gw] = False
            next_graph[gw][gwp] = False

            next_gw_links = gw_links.copy()
            next_gw_links.remove(gwl)            
            successors.append((gwl,AGENT,next_graph,next_gw_links,agentPos))

        else:
#        gw_links_sorted = sorted(list(gw_links),key=lambda x:gw_link_dangerosity(x,graph,agentPos) )
        for gwl in gw_links:
            gwp,gw = gwl
            
            next_graph = graph.copy()
            next_graph[gwp][gw] = False
            next_graph[gw][gwp] = False

            next_gw_links = gw_links.copy()
            next_gw_links.remove(gwl)            
            successors.append((gwl,AGENT,next_graph,next_gw_links,agentPos))

    elif player == AGENT:
        if agentPos in gwps:
            neighbors = graph[agentPos].nonzero()[0]
            for n in neighbors:
                if n in gws:
                    successors.append((n,PLAYER,graph,gw_links,n))
        else:
            closest_nodes = {shortest_path(graph, agentPos, gwp)[0] for gwp in gwps}
            for n in closest_nodes:
                successors.append((n,PLAYER,graph,gw_links,n))
    
    return successors
    
def max_value(state,alpha,beta) : 
    global node_counter
    node_counter += 1
    
    terminal_value = terminal(state)
    if terminal_value is not None:
        return (terminal_value,state[0])
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
    
    terminal_value = terminal(state)
    if terminal_value is not None:
        return (terminal_value,state[0])
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
start_time = time.time()

init_state = (None,PLAYER,graph,gw_links,si)
action = minimax(init_state)

duration = (time.time()-start_time)
print('Visited {} nodes in {:.3f} s'.format(node_counter, duration))