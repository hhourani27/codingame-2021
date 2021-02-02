import tkinter as tk
import pandas as pd
import random


class GameDisplay:
    def __init__(self,game):
        self.game = game
        
        # Window & Frame parameters
        self.window_title = 'Code of Kutulu'
        self.window_w = 1000
        self.window_h = 600
        self.canvas_w = 650
        self.canvas_h = self.window_h
        self.control_w = self.window_w - self.canvas_w
        self.control_h = self.window_h
        
        # Canvas/Game grid parameters
        maze_w,maze_h = [self.game.w, self.game.h]
        self.canvas_pad_cell = 1 # padding of canvas in cells
        self.grid_cell_size = min(
            self.canvas_w//(maze_w+1+2*self.canvas_pad_cell),
            self.canvas_h//(maze_h+1+2*self.canvas_pad_cell)
            )
        self.canvas_pad_x = (self.canvas_w - (maze_w+1)*self.grid_cell_size)//2
        self.canvas_pad_y = (self.canvas_h - (maze_h+1)*self.grid_cell_size)//2
        
        self.grid_tl_x = self.canvas_pad_x + self.grid_cell_size
        self.grid_tl_y = self.canvas_pad_y + self.grid_cell_size
        
        # color parameter
        self.grid_colors = {
            '.' : '#898989',
            '#' : '#464134',
            'w' : '#0e0f11'
            }
        
        self.player_colors = ['#FD1D5B','#22A1E4','#FA8C15','#6AC371']
        self.state_emoji = {
            'START': '🎬',
            'PANIC': '😨',
            'CALM': '😌',
            'DEAD': '⚰️'
            }
        
        # Font
        self.font = "Courier"
        self.font_size = 16
        
        # Game variables
        self.turn = 0
        
    def display(self):
        self.window=tk.Tk()
        self.window.title(self.window_title)
         
        # Display the control frame
        self.control_frame = tk.Frame(master=self.window, height=self.control_h, width=self.control_w, bg='white', relief=tk.RAISED, borderwidth=1)
        self.control_frame.grid_propagate(False)
        self.control_frame.grid(row=0, column=0)

        
        self.draw_control()
        
        
        # Display the game grid
        self.canvas = tk.Canvas(master=self.window, width=self.canvas_w, height=self.canvas_h, bg='white')
        self.canvas.grid(row=0,column=1)
        
        self.draw_grid()
        self.draw_entities()
                        
        self.window.mainloop()

    def draw_control(self):
        self.label_turn = tk.Label(master=self.control_frame, font=(self.font,self.font_size), bg='white',borderwidth=0,highlightthickness = 0)
        self.label_turn.grid(row=0, column=0, padx=20, pady=20)
        
        self.label_players = []
        for i in range(len(self.game.explorers)):
            label_players = tk.Label(master=self.control_frame, font=(self.font,self.font_size), bg='white', fg=self.player_colors[i],borderwidth=0,highlightthickness = 0)
            label_players.grid(row=(i+1)*2,column=0, padx=5, pady=5,sticky=tk.W)
            label_players2 = tk.Label(master=self.control_frame, font=(self.font,7), bg='white', fg=self.player_colors[i] ,borderwidth=0,highlightthickness = 0)
            label_players2.grid(row=(i+1)*2+1,column=0, padx=5, pady=5, sticky=tk.W)

            self.label_players.append((label_players,label_players2))
    
        self.update_labels()
        
        #Buttons        
        self.button_frame = tk.Frame(master=self.control_frame, bg='white', relief=tk.RAISED, borderwidth=1)
        self.button_frame.grid(row=(len(self.game.explorers)+1)*2, column=0, padx=20, pady=20)
        
        btn_start = tk.Button(master=self.button_frame, text='<<', command=self.start_turn)
        btn_start.grid(row=0, column=0)
        btn_dec = tk.Button(master=self.button_frame, text='<', command=self.dec_turn)
        btn_dec.grid(row=0, column=1)
        btn_inc = tk.Button(master=self.button_frame, text='>', command=self.inc_turn)
        btn_inc.grid(row=0, column=2)
        btn_end = tk.Button(master=self.button_frame, text='>>', command=self.end_turn)
        btn_end.grid(row=0, column=3)
    
    def update_labels(self):
        self.label_turn.config(text='Turn {}'.format(self.turn))
        
        for i,lbls_ex in enumerate(self.label_players):
            lbl1,lbl2 = lbls_ex
            ex = self.game.explorers[i]
            
            if self.turn <= ex.last_turn:
                info = ex.history[self.turn]
                txt = 'Player {} {} : {}'.format(i, self.state_emoji[info['state']], info['sanity'])
                txt2 = '{} : {}'.format(info['move'][0],info['move'][1])
            else:
                info = ex.history[-1]
                txt = 'Player {} {} : {}'.format(i, self.state_emoji[info['state']], info['sanity'])
                txt2 = '{} : {}'.format(info['move'][0],info['move'][1])
            lbl1.config(text = txt)
            lbl2.config(text = txt2)
        
    def draw_grid(self):
        
        # Draw column numbers
        for c in range(self.game.w):
            x = self.grid_tl_x + c*self.grid_cell_size + self.grid_cell_size//2
            y = self.grid_tl_y - self.grid_cell_size//2
            self.canvas.create_text(x,y,text=str(c))
        
        # Draw row numbers
        for r in range(self.game.h):
            x = self.grid_tl_x - self.grid_cell_size//2
            y = self.grid_tl_y + r*self.grid_cell_size + self.grid_cell_size//2
            self.canvas.create_text(x,y,text=str(r))
        
        # Draw grid      
        for x in range(self.game.w):
            for y in range(self.game.h):
                tl,br = self.cell_pos(x,y)
                color = self.grid_colors[self.game.maze[y][x]]
                
                
                self.canvas.create_rectangle(tl[0],tl[1],br[0],br[1], fill=color)

    def draw_entities(self):
        self.player_pawns = []
        for i in range(len(self.game.explorers)):
            ex = self.game.explorers[i]
            pawn = self.canvas.create_oval(0,0,self.grid_cell_size//2,self.grid_cell_size//2,fill=self.player_colors[i])
            self.player_pawns.append(pawn)
            
        self.update_entities()
            
    def update_entities(self):
        # Update explorer pawns
        pawn_size = self.grid_cell_size//2
        p_coords = [(0,0),(0,pawn_size),(pawn_size,0),(pawn_size,pawn_size)]
        
        for i,pawn in enumerate(self.player_pawns):
            ex = self.game.explorers[i]
            if self.turn <= ex.last_turn:
                pos = ex.history[self.turn]['pos']
            else:
                pos = ex.history[-1]['pos']
            
            tl,br = self.cell_pos(*pos)
            x = tl[0] + p_coords[i][0]
            y = tl[1] + p_coords[i][1]
            self.canvas.coords(self.player_pawns[i],x,y,x+pawn_size,y+pawn_size)
    
    def cell_pos(self,x,y):
        tl = (self.grid_tl_x + self.grid_cell_size*x, self.grid_tl_y + self.grid_cell_size*y)
        br = (self.grid_tl_x + self.grid_cell_size*(x+1), self.grid_tl_y + self.grid_cell_size*(y+1))
        return(tl,br)
    
    def update(self):
        self.update_labels()
        self.update_entities()
    
    def inc_turn(self):
        self.turn = min(self.turn+1,self.game.turns)
        self.update()
        
    def dec_turn(self):
        self.turn = max(self.turn-1,0)
        self.update()
        
    def start_turn(self):
        self.turn = 0
        self.update()
        
    def end_turn(self):
        self.turn = self.game.turns
        self.update()