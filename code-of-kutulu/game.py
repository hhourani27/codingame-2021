from mazes import mazes
import numpy as np
from collections import deque

class Explorer:
    def __init__(self,id,pos,player):
        self.id = id
        self.pos = pos
        
        # START, PANIC, CALM, DEAD
        self.state = 'START'
        self.sanity = 250
        
        self.last_turn = -1
        self.move = (None,None)
        
        self.player = player
        
        self.history = []
        self.update_history(turn=0)
        
    def update_history(self,turn):
        hist = {
            'turn': turn,
            'state': self.state,
            'pos': self.pos,
            'sanity': self.sanity,
            'move' : self.move
            }
        self.history.append(hist)
        
class Wanderer:
    def __init__(self,id,maze,w,h,pos,spawn_turn):
        self.id = id
        self.pos = pos
        self.maze = maze
        self.w = w
        self.h = h
        
        'SPAWNING', 'WANDERING', 'DISAPPEARED'
        self.state = 'SPAWNING'
        self.spawn_turn = spawn_turn
        self.target = None
        
        self.history = []
        
    def move(self,turn,live_explorers):
        if self.state == 'SPAWNING':
            if turn == self.spawn_turn + 2:
                self.state = 'WANDERING'
                self.target = self.closest_target(live_explorers)
        elif self.state == 'WANDERING':
            if self.target.state == 'DEAD':
                self.target = self.closest_target(live_explorers)
                
            self.pos = Game.shortest_path(self.maze, self.w, self.h, self.pos, self.target.pos)   
            
    def closest_target(self,explorers):
        closest_explorer = min(explorers, key=lambda x: Game.manhattan_distance(self.pos, x.pos))
        return closest_explorer
    
    def update_history(self,turn):
        hist = {
            'turn': turn,
            'state': self.state,
            'pos': self.pos,
            'target': self.target.id if self.target is not None else None,
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

        self.spawns = mazes[1]['spawns']
        self.spawn_first = 1
        self.spawn_freq = 3
        
        self.wanderer_count = 0
        self.wanderers = []
       
    def play(self):
        turn = 1
        # Move explorers
        while len(live_explorers := self.get_live_explorers()) > 1:
            # Update explorer position
            for ex in live_explorers:
                move = ex.player.next_move(ex.pos)
                if move != 'WAIT':
                    x,y = [int(p) for p in move[5:].split()]
                    if 0 <= x < self.w and 0 <= y < self.h and self.maze[y][x] != '#':
                        if (x,y) != ex.pos:
                            next_pos = self.shortest_path(self.maze,self.w,self.h,fr=ex.pos, to=(x,y))
                            if next_pos is not None:
                                move_result = 'Go from {} to {} : {}'.format(ex.pos,(x,y),next_pos)
                                ex.pos = next_pos
                            else:
                                move_result = 'Can\'t reach cell {}'.format((x,y))
                        else:
                            move_result = 'Same position {}'.format((x,y))
                    else:
                        move_result = 'Invalid move'
                else:
                    move_result = 'Wait'
                    
                ex.move = (move,move_result)
                
            # Spawn Wanderers
            if (turn-1) % 5 == 0:
                spawns = self.farthest_spawns()
                for s in spawns:
                    new_wanderer = Wanderer(self.wanderer_count,self.maze,self.w,self.h,s,turn)
                    self.wanderers.append(new_wanderer)
                    self.wanderer_count += 1
                
            # Move Wanderers
            live_wanderes = self.get_live_wanderers()
            for w in live_wanderes:
                w.move(turn,live_explorers)
            
            # Wanderers Attack
            for w in live_wanderes:
                for ex in live_explorers:
                    if w.pos == ex.pos:
                        w.state = 'DISAPPEARED'
                        ex.sanity -= 20
            
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
                    
            
            # Finish & update history
            for ex in live_explorers:
                ex.last_turn = turn
                ex.update_history(turn)
            for w in live_wanderes:
                w.update_history(turn)
            
            turn += 1
        
        self.turns = turn-1
            
    def get_live_explorers(self):
        return [ex for ex in self.explorers if ex.state != 'DEAD']
    
    def get_live_wanderers(self):
        return [w for w in self.wanderers if w.state != 'DISAPPEARED']
    
    def is_next_to_another_explorer(self,ex):
        for eo in self.get_live_explorers():
            if eo != ex:
                if self.manhattan_distance(ex.pos,eo.pos) <= 2:
                    return True
        return False
    
    @staticmethod
    def shortest_path(maze,w,h,fr,to):
        if fr == to:
            return to
        
        xf,yf = fr
        xt,yt = to
        
        frontier = deque()
        frontier.append((xt,yt))
        came_from = dict()
        came_from[(xt,yt)] = None
        
        while len(frontier) > 0:
            curr = frontier.popleft()
            x,y = curr
            
            if curr == fr:
                break
            
            adjacent_cells= [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
            next_cells = [(xn,yn) for xn,yn in adjacent_cells \
                     if 0 <= xn < w and 0 <= yn < h and maze[yn][xn] != '#']
                
            for next in next_cells:
                if next not in came_from:
                    frontier.append(next)
                    came_from[next] = curr
        
        return came_from[fr] if fr in came_from else None

    
    def farthest_spawns(self):      
        distances = np.zeros((4,len(self.spawns)),dtype=np.int8)
        for s,s_pos in enumerate(self.spawns):
            for e,ex in enumerate(self.get_live_explorers()):
                distances[e,s] = self.manhattan_distance(s_pos,ex.pos)
                
        max_dist = np.amax(distances)
        farthest_spawns_id = np.where(distances == max_dist)[1]
        return [s for i,s in enumerate(self.spawns) if i in farthest_spawns_id]
    
    @staticmethod
    def manhattan_distance(a,b):
        xa,ya = a
        xb,yb = b
        return abs(xa-xb) + abs(ya-yb)