import random

class PlayerRandom:
    def __init__(self):
        pass
    
    def set_maze(self,w,h,maze):
        self.w = w
        self.h = h
        self.maze = maze
    
    def next_move(self,pos):
        x,y = pos
        adjacent_cells= [(x,y),(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        legal_moves = [(xn,yn) for xn,yn in adjacent_cells \
                     if 0 <= xn < self.w and 0 <= yn < self.h and self.maze[yn][xn] not in ['#','w']]
            
        new_pos = random.choice(legal_moves)
        if new_pos == pos:
            return 'WAIT'
        else :
            return 'MOVE {} {}'.format(new_pos[0],new_pos[1])