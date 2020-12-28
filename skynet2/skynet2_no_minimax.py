import numpy as np
from collections import deque
from test_cases import test_cases
import time

#%% Game Input
test_case = test_cases[2]
v,e,g,graph,gws,agent =[k[1] for k in test_case.items()]

#%% Game init

# Return all neighbors of a node
def get_neighbors(graph, n):
    return graph[n].nonzero()[0]

# Return a set of links to a gw : (gwp,gw)
def get_gw_links(graph, gws):
    gw_links = set()
    for gw in gws:
        gwps = get_neighbors(graph, gw)
        for gwp in gwps:
            gw_links.add((gwp,gw))
    return gw_links

# Return a set of all nodes that are parent to a gw
def get_gwps(gw_links):
    return {gwp for gwp,gw in gw_links}

# Return all links with a gw having as parent gwp
def get_gw_links_of_gwp(gw_links,gwp):
    return [link for link in gw_links if link[0] == gwp]

# Get the GW degree of a gwp : number of connected gws
def get_gw_degree(gw_links,gwp):
    return len(get_gw_links_of_gwp(gw_links,gwp))

def get_shortest_path(graph,gws,start,goal):
    frontier = deque([start])
    parent = {start:None}
    
    while len(frontier) > 0:
        current = frontier.popleft()
        if current == goal:
            break
        if current in gws:
            continue
        neighbors = get_neighbors(graph, current)
        for n in neighbors:
            if n not in parent:
                frontier.append(n)
                parent[n] = current
                
    path = []
    while current != start:
        path.insert(0, current)
        current = parent[current]
    return path

# Return the closest nodes to an agent (first one if there are multiple)
def get_closest_node_to_agent(graph,gws,nodes,agent):
    min_distance = 1000
    distances = dict()
    
    for n in nodes:
        shortest_path = get_shortest_path(graph,gws,agent,n)
        dist = len(shortest_path)
        if dist < min_distance:
            min_distance = dist
        distances[n] = dist
        
    for n,dist in distances.items():
        if dist == min_distance:
            return n


gw_links = get_gw_links(graph, gws)
gwps = get_gwps(gw_links)

#%% Turn input

# Play
start_time = time.time()

# If agent is a gwp => sever link to GW
if agent in gwps:
    link_to_sever = get_gw_links_of_gwp(gw_links, agent)[0]
    
else:
    gwps = get_gwps(gw_links)
    gwps_degree_multi = list(filter(lambda gwp: get_gw_degree(gw_links,gwp) > 1,gwps))
    # If there are gwps with GW_degree > 1
    if len(gwps_degree_multi) > 1:
        nbr_not_gwp_in_path = dict()
        for gwp in gwps_degree_multi: # for each gwp with gw_degree > 1
            path = get_shortest_path(graph, gws, agent, gwp)
            count = sum(map(lambda x: 1 if x not in gwps else 0,path))
            nbr_not_gwp_in_path[gwp] = count
        min_count = min(nbr_not_gwp_in_path.values())
        for gwp in gwps_degree_multi:
            if nbr_not_gwp_in_path[gwp] == min_count:
                link_to_sever = get_gw_links_of_gwp(gw_links, gwp)[0]
                break
    else: # all gwp have gw_degree = 1
        # get the closest gwp and sever its link
        closest_gwp = get_closest_node_to_agent(graph, gws, gwps, agent)
        link_to_sever = get_gw_links_of_gwp(gw_links, closest_gwp)[0]

gwp,gw = link_to_sever
print("{} {}".format(gwp,gw))
duration = (time.time()-start_time)

#%% modify input
