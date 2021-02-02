from mazes import mazes
import numpy as np
import random

class Explorer:
    def __init__(self,id,pos,player):
        self.id = id
        self.pos = pos
        
        # START, PANIC, CALM, DEAD
        self.state = 'START'
        self.sanity = 250
        self.last_turn = -1
        
        self.player = player
        
        self.history = []
        self.update_history(turn=0)
        
    def update_history(self,turn):
        hist = {
            'turn': turn,
            'state': self.state,
            'pos': self.pos,
            'sanity': self.sanity
            }
        self.history.append(hist)

class Game:
    def __init__(self,players):
        
        # Global game info (that doesn't change)
        maze_nb = 1
        self.maze = mazes[maze_nb]['maze']
        self.w = mazes[maze_nb]['w']
        self.h = mazes[maze_nb]['h']
            
        self.explorers = []
        explorers_pos = mazes[1]['explorers']
        for id in range(len(players)):
            p = players[id]
            p.set_maze(self.w, self.h, self.maze)
            ex = Explorer(id,explorers_pos[id],p)
            self.explorers.append(ex)

        
        
        """self.spawns = mazes[1]['spawns']
        self.spawn_first = 2
        self.spawn_freq = 3"""
       
    def play(self):
        turn = 1
        while len(live_explorers := self.get_live_explorer()) > 1:
            # Update explorer position
            for ex in live_explorers:
                move = ex.player.next_move(ex.pos)
                if move != 'WAIT':
                    x,y = [int(p) for p in move[5:].split()]
                    ex.pos = (x,y)
            
            # Update explorer's sanity
            for ex in live_explorers:
                if self.is_next_to_another_explorer(ex):
                    ex.state = 'CALM'
                    ex.sanity -= 1
                else:
                    ex.state = 'PANIC'
                    ex.sanity -= 3
                    
            # Check if there are dead explorers
            for ex in live_explorers:
                if ex.sanity <= 0:
                    ex.state = 'DEAD'
                    
            
            # Finish & update history of explorers
            for ex in live_explorers:
                ex.last_turn = turn
                ex.update_history(turn)
            
            turn += 1
        
        self.turns = turn-1
            
    def get_live_explorer(self):
        return [ex for ex in self.explorers if ex.state != 'DEAD']
    
    def is_next_to_another_explorer(self,ex):
        for eo in self.get_live_explorer():
            if eo != ex:
                if self.manhattan_distance(ex.pos,eo.pos) <= 2:
                    return True
        return False
    
    def farthest_spawns(self):
        distances = np.zeros((4,len(self.spawns)),dtype=np.int8)
        for s,s_pos in enumerate(self.spawns):
            for e,e_pos in enumerate(self.explorers_pos):
                distances[e,s] = self.manhattan_distance(s_pos,e_pos)
                
        max_dist = np.amax(distances)
        farthest_spawns = np.where(distances == max_dist)[1]
        return farthest_spawns
    
    @staticmethod
    def manhattan_distance(a,b):
        xa,ya = a
        xb,yb = b
        return abs(xa-xb) + abs(ya-yb)