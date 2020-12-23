from game import Game
import numpy as np
import random

random.seed(1)

def updateMode(maze, mode, player_position):
    new_mode = mode
    if mode == 'EXPLORE':
        if maze[maze == 'C'].size == 1:
            new_mode = 'SEARCH_PATH_TO_CONTROL_ROOM'
    if mode == 'SEARCH_PATH_TO_CONTROL_ROOM':
        if maze[player_position] == 'C':
            new_mode = 'BACK_TO_INITIAL_POSITION'
    if mode == 'BACK_TO_INITIAL_POSITION':
        if maze[player_position] == 'T':
            new_mode = 'FINISH'
            
    return new_mode

# Using BFS, find the closest fog (?) and output direction to it
def explore(maze, player_position):
    frontier = list()
    frontier.append(player_position)
    came_from = dict()
    came_from[player_position] = None
    
    while len(frontier) > 0:
        current_cell = frontier.pop(0)
        
        # If I found a fog (?) return
        if(maze[current_cell] == '?'):
            break
        
        x,y = current_cell
        r,c = maze.shape
        next_cells = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        next_cells = list(filter(lambda n: n[0]>=0 and n[0] < r and n[1] >= 0 and n[1] < c, next_cells))
        next_cells = list(filter(lambda n: maze[n] != '#',next_cells))
        for next in next_cells:
            if next not in came_from:
                frontier.append(next)
                came_from[next] = current_cell
    
    # after finding a (?) backtrack through the shortest path from player position and return the action
    while True:
        prev_cell = came_from[current_cell]
        if prev_cell == player_position:
            prev_cell = came_from[current_cell]
            if player_position[0] < current_cell[0]: 
                return 'DOWN'
            elif current_cell[0] < player_position[0]:
                return 'UP'
            elif player_position[1] < current_cell[1]:
                return 'RIGHT'
            elif current_cell[1] < player_position[1]:
                return 'LEFT'
            else:
                return None
        else:
            current_cell = prev_cell

# Using BFS, find the shortest path from player_position to goal_positionand output direction to it
# assumer that (?) are walkable cells
def shortest_path(maze, player_position, goal_position):
    frontier = list()
    frontier.append(player_position)
    came_from = dict()
    came_from[player_position] = None
    
    while len(frontier) > 0:
        current_cell = frontier.pop(0)
        
        # If I found a fog (?) return
        if(current_cell == goal_position):
            break
        
        x,y = current_cell
        r,c = maze.shape
        next_cells = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        next_cells = list(filter(lambda n: n[0]>=0 and n[0] < r and n[1] >= 0 and n[1] < c, next_cells))
        next_cells = list(filter(lambda n: maze[n] != '#',next_cells))
        for next in next_cells:
            if next not in came_from:
                frontier.append(next)
                came_from[next] = current_cell
    
    # after finding a (?) backtrack through the shortest path from player position and return the action
    while True:
        prev_cell = came_from[current_cell]
        if prev_cell == player_position:
            prev_cell = came_from[current_cell]
            if player_position[0] < current_cell[0]: 
                return 'DOWN'
            elif current_cell[0] < player_position[0]:
                return 'UP'
            elif player_position[1] < current_cell[1]:
                return 'RIGHT'
            elif current_cell[1] < player_position[1]:
                return 'LEFT'
            else:
                return None
        else:
            current_cell = prev_cell

       

#%%

game = Game(5,5)

r,c = game.getSize()

# mode values
# EXPLORE
# SEARCH_PATH_TO_CONTROL_ROOM
# BACK_TO_INITIAL_POSITION
# FINISH
mode = 'EXPLORE'


while True:
    kr, kc = game.getPlayerPosition()
    maze = game.getMaze()
    
    print(game.getMaze(True))
    
    mode = updateMode(maze, mode, (kr,kc))
    print(mode)
    action =''
    
    if(mode == 'EXPLORE'):
        action = explore(maze,(kr,kc))
    if(mode == 'SEARCH_PATH_TO_CONTROL_ROOM'):
        control_room_position = list(zip(*np.where(maze == 'C')))[0]
        action = shortest_path(maze, (kr,kc),control_room_position)
    if(mode == 'BACK_TO_INITIAL_POSITION'):
        initial_position = list(zip(*np.where(maze == 'T')))[0]
        action = shortest_path(maze, (kr,kc),initial_position)
    if(mode == 'FINISH'):
        break
    
    print(action)
    game.move(action)       
