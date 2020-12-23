from maze import Maze
import random
import numpy as np


class Game:
    def __init__(self, rows, cols):
       
        #Generate maze
        maze = np.array(Maze.generate(rows, cols)._to_str_matrix())
        self.rows = maze.shape[0]
        self.cols = maze.shape[1]
        
        maze[maze == 'O'] = '#'
        maze[maze == ' '] = '.'
        
        #Choose initial and control room location
        empty_cells = list(zip(*np.nonzero(maze == '.')))
        random_locations = random.sample(empty_cells,2)
        
        self.initial_position = random_locations[0]
        self.control_room_position = random_locations[1]
        
        self.player_position = self.initial_position
        
        
        maze[self.initial_position] = 'T'
        maze[self.control_room_position] = 'C'
        self.maze = maze
        
        #Initialize fogged maze
        self.visibility_window_size = 2
        self.visibility_matrix = np.full(self.maze.shape, False)
        self.updateVisibilityMatrix()
        
    def updateVisibilityMatrix(self):
        pp = self.player_position
        vw = self.visibility_window_size
        window = self.visibility_matrix[max(0,pp[0]-vw):min(self.rows,pp[0]+vw+1),max(0,pp[1]-vw):min(self.cols,pp[1]+vw+1)]
        window[:] = True
        
    def getMaze(self, player = False):
        fogged_maze = self.maze.copy()
        vw = self.visibility_matrix
        vwi = np.invert(vw)
        fogged_maze[vwi] = '?'
        
        if player is True:
            fogged_maze[self.player_position] = 'P'
        
        return fogged_maze
    
    def move(self,direction):
        r,c = self.player_position
        if direction == 'UP':
            r -= 1
        elif direction == 'DOWN':
            r += 1
        elif direction == 'RIGHT':
            c += 1
        elif direction == 'LEFT':
            c -= 1
        else :
            return None
        
        if r < 0 or r >= self.rows:
            return None
        if c < 0 or c >= self.cols:
            return None
        if self.maze[r,c] == '#':
            return None
        
        self.player_position = (r,c)
        self.updateVisibilityMatrix()
        
    def getPlayerPosition(self):
        return self.player_position
    
    def getSize(self):
        return (self.rows, self.cols)
