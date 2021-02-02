import random

class PlayerRandom:
    def __init__(self):
        # ADJACENT_CELL, RANDOM_CELL
        self.mode = 'RANDOM_CELL'
        pass
    
    def set_maze(self,w,h,maze):
        self.w = w
        self.h = h
        self.maze = maze
    
    def next_move(self,pos):
        x,y = pos
        
        if self.mode == 'ADJACENT_CELL':
            adjacent_cells= [(x,y),(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
            legal_moves = [(xn,yn) for xn,yn in adjacent_cells \
                         if 0 <= xn < self.w and 0 <= yn < self.h and self.maze[yn][xn] not in ['#','w']]            
            new_pos = random.choice(legal_moves)
            
        elif self.mode == 'RANDOM_CELL':
            new_pos = (random.randrange(0,self.w),random.randrange(0,self.h))

        if new_pos == pos:
            return 'WAIT'
        else :
            return 'MOVE {} {}'.format(new_pos[0],new_pos[1])