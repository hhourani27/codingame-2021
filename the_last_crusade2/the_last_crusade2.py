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

rleft = [0,1,3,2,5,4,9,6,7,8,13,10,11,12]
rright = [0,1,3,2,5,4,7,8,9,6,11,12,13,10]

TC = test_cases[4]

w,h = (TC['w'],TC['h'])
grid = TC['grid']
ex = TC['ex']

grid = np.array(grid)

#%%
xi, yi, posi = [TC['xi'], TC['yi'], TC['posi']]
r = TC['r']

state_count = 0
def dfs(grid,xi,yi,posi,actions,rocks):
    global state_count
    if state_count < 1000:
        print('{:03}: {} - {} {}'.format(state_count,actions,xi,yi))
    state_count += 1
    
    # If Indy enterd the exit room than wooho!
    if (xi,yi) == (ex,h-1):
        return actions
    
    room_type = grid[yi,xi]   
    room = rooms[abs(room_type)]
    # (A) Indy struck a wall before entry or entered and can't exit from the room
    if posi not in room:
        return False

    next_actions = []

    # (B) Calculate next room
    exit_pos = room[posi]
    if exit_pos == 'DOWN':
        next_xi,next_yi = (xi,yi+1)
        next_posi = 'TOP'
    elif exit_pos == 'LEFT':
        next_xi,next_yi = (xi-1,yi)
        next_posi = 'RIGHT'
    elif exit_pos == 'RIGHT':
        next_xi,next_yi = (xi+1,yi)
        next_posi = 'LEFT'
    
    # (B.0) Indy is hitting the border of the grid:
    if next_xi < 0 or next_xi >= w or next_yi < 0 or next_yi >= h:
        return False    
    
    next_room_type = grid[next_yi,next_xi]    
    next_room = rooms[abs(next_room_type)]
    
    # (B.1) If Indy is gona hit a wall when exiting then only actions are to rotate next room
    if next_posi not in next_room:
        # If I can't rotate next room than all is lost
        if next_room_type <= 0:
            return False
        # Else try to rotate the room
        else:
            for r in ['RIGHT','LEFT']:
                next_room_type_r = rleft[next_room_type] if r=='LEFT' else rright[next_room_type]
                next_room = rooms[next_room_type_r]
                if next_posi in next_room:
                    next_actions = actions + [(next_xi,next_yi,r)]
                    next_grid = np.copy(grid)
                    next_grid[next_yi,next_xi] = next_room_type_r
                    result = dfs(next_grid,next_xi,next_yi,next_posi,next_actions,rocks)
                    if result != False:
                        return result
                
            # Rotating the next room didn't work, all is lost
            return False
            
        
    # (C) else if Indy is gona pass to the next room without problem, then you have much more options
    else:
        # Try to wait
        next_actions = actions + ['WAIT']
        result = dfs(grid,next_xi,next_yi,next_posi,next_actions,rocks)
        if result != False:
            return result
        
        # Try all possible rotations
        for y in range(yi,h):
            for x in range(w):
                if grid[y,x] > 0 and (x,y) != (xi,yi):
                    for r in ['RIGHT','LEFT'] :
                        next_actions = actions + [(x,y,r)]
                        next_grid = np.copy(grid)
                        next_grid[y,x] = rleft[grid[y,x]] if r == 'LEFT' else rright[grid[y,x]]
                        result = dfs(next_grid,next_xi,next_yi,next_posi,next_actions,rocks)
                        if result != False:
                            return result
        return False
    
#%%
result = dfs(grid,xi,yi,posi,[],[])
print('RESULT=====')
print(result)
#for r in result:
#    print(r)
    