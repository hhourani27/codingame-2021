import numpy as np
from test_cases import test_cases

rooms = [
    {},
    {'TOP':'DOWN','LEFT':'DOWN','RIGHT':'DOWN'},
    {'LEFT':'RIGHT','RIGHT':'LEFT'},
    {'TOP':'DOWN'},
    {'TOP':'LEFT','RIGHT':'DOWN'},
    {'TOP':'RIGHT','LEFT':'DOWN'},
    {'LEFT':'RIGHT','RIGHT':'LEFT'},
    {'TOP':'DOWN','RIGHT':'DOWN'},
    {'LEFT':'DOWN','RIGHT':'DOWN'},
    {'TOP':'DOWN','LEFT':'DOWN'},
    {'TOP':'LEFT'},
    {'TOP':'RIGHT'},
    {'RIGHT':'DOWN'},
    {'LEFT':'DOWN'}
    ]

rooms_rotations = [
    [], #0
    [], #1
    [(3,'RIGHT',1)], #2
    [(2,'RIGHT',1)], #3
    [(5,'RIGHT',1)], #4
    [(4,'RIGHT',1)], #5
    [(7,'RIGHT',1),(9,'LEFT',1),(8,'RIGHT',2)], #6
    [(8,'RIGHT',1),(6,'LEFT',1),(9,'RIGHT',2)], #7
    [(9,'RIGHT',1),(7,'LEFT',1),(6,'RIGHT',2)], #8
    [(6,'RIGHT',1),(8,'LEFT',1),(7,'RIGHT',2)], #9
    [(11,'RIGHT',1),(13,'LEFT',1),(12,'RIGHT',2)], #10
    [(12,'RIGHT',1),(10,'LEFT',1),(13,'RIGHT',2)], #11
    [(13,'RIGHT',1),(11,'LEFT',1),(10,'RIGHT',2)], #12
    [(10,'RIGHT',1),(12,'LEFT',1),(11,'RIGHT',2)], #13
    ]

#%% Inputs

TC = test_cases[6.1]

w,h = (TC['w'],TC['h'])
grid = TC['grid']
ex = TC['ex']

xi, yi, posi = [TC['xi'], TC['yi'], TC['posi']]
r = TC['r']
if r > 0:
    rocks = TC['rocks']

grid = np.array(grid)

#%%
state_count = 0
def get_all_paths_for_indy(grid,xi,yi,posi):
    
    # state = grid,xi,yi,posi, current room type, path so far, rotations so far, cost so far
    stack = [(xi,yi,posi,grid[yi,xi],[(xi,yi,grid[yi,xi])],[],1)]
    
    successful_paths = []
    
    while len(stack) > 0:
        global state_count
        state_count += 1
        
        curr = stack.pop()
        x,y,pos,room_type,path,rotations,cost  = curr
        
        # If Indy enterd the exit room than wooho!
        if (x,y) == (ex,h-1):
            successful_paths.append((path,rotations))
            continue
        
        # Else Compute next position and room
        exit_pos = rooms[abs(room_type)][pos]
        if exit_pos == 'DOWN':
            next_x,next_y = (x,y+1)
            next_pos = 'TOP'
        elif exit_pos == 'LEFT':
            next_x,next_y = (x-1,y)
            next_pos = 'RIGHT'
        elif exit_pos == 'RIGHT':
            next_x,next_y = (x+1,y)
            next_pos = 'LEFT'
        
        # If I'm not going outside the grid
        if 0 <= next_x < w and 0 <= next_y < h :
            next_room_type = grid[next_y,next_x]
            # Compute the possible rotations I can apply to the next room
            if next_room_type != 0: # If next room is not a block of type 0
                # If I can rotate the room
                possible_rotations = \
                    [(next_room_type,None,0)] + rooms_rotations[next_room_type] if next_room_type > 0 \
                    else [(next_room_type,None,0)]
                    
                for r in possible_rotations:
                    next_room_type_r,direction,cost_r = r
                    if cost_r <= cost: # If I have enough budget to rotate the room
                        if next_pos in rooms[abs(next_room_type_r)]: # If I can enter the rotated room
                            next_path = path + [(next_x,next_y,next_room_type_r)]
                            next_rotations = rotations + [(next_x,next_y,direction)]*cost_r if direction is not None else rotations
                            next_cost = cost - cost_r + 1
                            next_state = \
                                (next_x,next_y,next_pos,next_room_type_r,next_path,next_rotations,next_cost)
                            
                            stack.append(next_state)
                                
    return successful_paths

def get_all_paths_for_rocks(grid,xi,yi,posi):
    
    # state = grid,xi,yi,posi, current room type, path so far, rotations so far, cost so far
    stack = [(xi,yi,posi,grid[yi,xi],[(xi,yi,grid[yi,xi])],[])]
    
    successful_paths = []
    
    while len(stack) > 0:
        curr = stack.pop()
        x,y,pos,room_type,path,rotations  = curr
        
        # If rock enterd the exit room than wooho!
        if (x,y) == (ex,h-1):
            successful_paths.append((path,rotations))
            continue
        
        # Else Compute next position and room
        exit_pos = rooms[abs(room_type)][pos]
        if exit_pos == 'DOWN':
            next_x,next_y = (x,y+1)
            next_pos = 'TOP'
        elif exit_pos == 'LEFT':
            next_x,next_y = (x-1,y)
            next_pos = 'RIGHT'
        elif exit_pos == 'RIGHT':
            next_x,next_y = (x+1,y)
            next_pos = 'LEFT'
            
        # if rocks will be going ouside the grid then woohoo!
        if next_x < 0 or next_x >= w or next_y < 0 or next_y >= h:
            successful_paths.append((path,rotations))
            continue
           
        # If rock will be continuing inside the grid
        else:
            next_room_type = grid[next_y,next_x]
            
            # if a rock hit a wall when entering the new room then woohoo!
            if next_pos not in rooms[abs(next_room_type)]:
                 successful_paths.append((path,rotations))
                 
                 # then find ways to rotate the room and let it pass (so it may hit another rock)
                 if next_room_type > 0:
                     possible_rotations = rooms_rotations[next_room_type]
                    
                     for r in possible_rotations:
                        next_room_type_r,direction,cost_r = r
                        next_rotations = rotations + [(next_x,next_y,direction)]*cost_r
                        if next_pos in rooms[abs(next_room_type_r)]:
                            next_path = path + [(next_x,next_y,next_room_type_r)]
                            next_state = \
                                    (next_x,next_y,next_pos,next_room_type_r,next_path,next_rotations)
                            stack.append(next_state)
            
            # else, let it pass and then find a way to make it hit a wall
            else:
                next_path = path + [(next_x,next_y,next_room_type)]
                next_state = \
                            (next_x,next_y,next_pos,next_room_type,next_path,rotations)
                stack.append(next_state)
                
                if next_room_type > 0:
                    possible_rotations = rooms_rotations[next_room_type]
                    for r in possible_rotations:
                        next_room_type_r,direction,cost_r = r
                        next_rotations = rotations + [(next_x,next_y,direction)]*cost_r
                        if next_pos not in rooms[abs(next_room_type_r)]:
                            successful_paths.append((path,next_rotations))
                            break

                        
    return successful_paths



#%%
possible_solutions_indy = get_all_paths_for_indy(grid,xi,yi,posi)
path_indy,rotations_indy = possible_solutions_indy[0]
actions = rotations_indy + ['WAIT']*(len(path_indy)-len(rotations_indy))

if r > 0:
    possible_solution_rocks = []
    for xr, yr, posr in rocks:
        possible_solution_rocks.append(get_all_paths_for_rocks(grid,xr,yr,posr))
    
    combinations = [(a,b) for a in possible_solutions_indy for b in possible_solution_rocks]