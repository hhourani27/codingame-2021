import pandas as pd
from game_display import GameDisplay

from game import Game
from player_random import PlayerRandom

# setup game
players = [PlayerRandom() for i in range(4)]
game = Game(players)

# play game
game.play()

#%%
# display game
display = GameDisplay(game)
display.display()

#%%
