# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:10:27 2020

@author: hhour
"""

import random
import numpy as np

#random.seed(27)

class Shape:
    def __init__(self, id, width, height, definition) :
        self.id = id
        self.width = width
        self.height = height
        self.definition = definition
        
        # compute representation of each shape
        flat_definition = list(self.definition)
        self.cellCount = flat_definition.count('#')
        
            # replace # by numbers
        n = 1
        for i in range(len(flat_definition)):
            if flat_definition[i] == '#':
                flat_definition[i] = n
                n += 1
            else :
                flat_definition[i] = -1
        
        repr_2d = np.array(flat_definition).reshape((self.width, self.height), order='F')
        
        self.permutations = [None]*2
        for flip in [0,1]:
            self.permutations[flip] = [None]*4
            for rotate in [0,1,2,3]:
                ar = repr_2d.copy()
                if flip == 1:
                    ar = np.rot90(np.fliplr(ar))
                ar = np.rot90(ar,rotate)
                self.permutations[flip][rotate] = ar
                        
        
    def __repr__(self):
        return self.id
    
    def __hash__(self):
        return ord(self.id)
        
    def printPermutations(self):
        for flip in [0,1]:
            for rotate in [0,1,2,3]:
                print(self.id + str(flip) + str(rotate))
                print(self.permutations[flip][rotate].transpose())

# [turn, shapeSize, shapeScore, distanceFromCenter, distanceFromAnotherPlayer]
class Strategy:
    def __init__(self,id,weights):
        self.id = id
        self.weights = weights
        
    @staticmethod
    def createRandomStrategy(id):
        return Strategy(id,[random.uniform(-1,1) for i in range(5)])
    
    @staticmethod
    def createStrategy(id,weights):
        return Strategy(id,weights)
        
class Player:
    def __init__(self,id,shapes,strategy):
        self.id = id
        self.shapes = shapes
        self.status = 'PLAYING'
        self.score = 0
        self.strat = strategy
        
    def __repr__(self):
        return 'Player ' + str(self.id) + ' ' + str(self.shapes)
        
    def playTurn(self, turn, board, legalMoves, playerCount):
        if len(legalMoves) == 0:
            return None
        else:
            scores = [0.0]*len(legalMoves)
            for i, move in enumerate(legalMoves):
                score = self.evaluateMove(turn, board, move, playerCount)
                scores[i] = score
            maxScore = max(scores)
            chosenMoves = [legalMoves[i] for i,s in enumerate(scores) if s == maxScore]
            chosenMove = random.choice(chosenMoves);
            self.shapes.remove(chosenMove.shape)
            return chosenMove
        
    def evaluateMove(self, turn, board, move, playerCount):
        turn_N = 0
        if playerCount == 2:
            turn_N = turn/28
        elif playerCount == 3:
            turn_N = turn/31
        else:
            turn_N = turn/36
        
        shape = move.shape
        shapeSize_N = shape.width*shape.height/9
        shapeScore_N = shape.cellCount/5
        
        distanceFromCenter_N = move.distanceFromCenter()/12
        
        touchedCells = move.touchedCells
        opponentCells = []
        for i in range(13):
            for j in range(13):
                if board[i][j] != '.' and board[i][j] != str(self.id):
                    opponentCells.append((i,j))
                    
        minDistance = 26
        for cell in touchedCells:
            for opp in opponentCells:
                dist = abs(cell[0]-opp[0])+abs(cell[1]-opp[1])
                if dist < minDistance:
                    minDistance = dist
        distanceFromAnotherPlayer_N = minDistance/26
        
        w = self.strat.weights                    
        score = (w[0]*turn_N + w[1]*shapeSize_N + w[2]*shapeScore_N + w[3]*distanceFromCenter_N + w[4]*distanceFromAnotherPlayer_N)/sum(w)
        
        #return score
        return 0.0

class  Move:
    
    cache = dict()
    
    def __init__(self,shape,flip,rotate,connectedValue,positionCell):
        self.shape = shape
        self.flip = flip
        self.rotate = rotate
        self.connectedValue = connectedValue
        self.positionCell = positionCell
        self.touchedCells = self.touchedCells()
        
    def touchedCells(self) :
        key = self.__repr__()
        if key in Move.cache:
            return Move.cache[key]
        
        representation = self.shape.permutations[self.flip][self.rotate] 
        (sr,sc) = (-1,-1)
        for i in range(representation.shape[0]):
            for j in range(representation.shape[1]):
                if representation[i][j] == self.connectedValue:
                    (sr,sc) = (i,j)
                
        (pr,pc) = self.positionCell
        
        touchedCells = np.empty(representation.shape,dtype=object)
        for i in range(representation.shape[0]):
            for j in range(representation.shape[1]):
                if representation[i][j] != -1:
                    touchedCells[i][j] = (pr+i-sr,pc+j-sc)
                else:
                    touchedCells[i][j] = None
                    
        touchedCells = touchedCells.flatten()
        touchedCells = touchedCells[touchedCells!=None]
        
        Move.cache[key] = touchedCells        
        return touchedCells
    
    def distanceFromCenter(self):
        minDistance = 100
        for cell in self.touchedCells:
            dist = abs(cell[0]-6)+abs(cell[1]-6)
            if dist < minDistance:
                minDistance = dist
        
        return minDistance
    
    def __repr__(self):
        return 'Move ' + str(self.positionCell[0]) + ' ' + str(self.positionCell[1]) \
            + ' ' + str(self.shape.id) \
            + str(self.flip) + str(self.rotate) + str(self.connectedValue)

    def __hash__(self):
        return 2**hash(self.shape) * 3**self.positionCell[0] * 5**self.positionCell[1] \
            * 7**self.connectedValue * 13**self.flip * 17**self.rotate

shapes = [
    Shape('A',1,1,'#'),
    Shape('B',2,1,'##'),
    Shape('C',3,1,'###'),
    Shape('D',2,2,'###.'),
    Shape('E',4,1,'####'),
    Shape('F',3,2,'####..'),
    Shape('G',3,2,'###.#.'),
    Shape('H',2,2,'####'),
    Shape('I',3,2,'##..##'),
    Shape('J',5,1,'#####'),
    Shape('K',4,2,'#####...'),
    Shape('L',4,2,'####.#..'),
    Shape('M',4,2,'###...##'),
    Shape('N',3,2,'#####.'),
    Shape('O',3,2,'####.#'),
    Shape('P',3,3,'####..#..'),
    Shape('Q',3,3,'###.#..#.'),
    Shape('R',3,3,'##..#..##'),
    Shape('S',3,3,'##..##..#'),
    Shape('T',3,3,'##..##.#.'),
    Shape('U',3,3,'.#.###.#.')
    ]


class Game:
    def __init__(self, playerCount, strategies):
        self.playerCount = playerCount
        
        # Determining number of shapes for each player
        if playerCount == 2: 
            self.shapesPerPlayerCount = 18
        elif playerCount == 3:
            self.shapesPerPlayerCount = 13
        elif playerCount == 4:
            self.shapesPerPlayerCount = 10
            
        # Choose the shapes that will be played
        self.shapesToPlay = shapes[:4]
        self.shapesToPlay.extend(random.sample(shapes[4:],self.shapesPerPlayerCount-4))
        
        # Initialize players
        self.players = []       
        for i in range(self.playerCount):
            self.players.append(Player(i,self.shapesToPlay.copy(),strategies[i]))
            
        # Initialize board
        self.board = np.full((13,13),'.')
            
        self.status = 'INIT'
            
    def start(self):
        print('STARTING GAME')
        self.status = 'RUN'
        turn = 1
        currPlayerId = 0
        
        # Game loop
        while currPlayerId is not None:
            print('Turn ' + str(turn))
            player = self.players[currPlayerId]
            print(str(player) + ' to play')
            legalMoves = Game.computeLegalMoves(self.board, turn, player)
            print('Player ' + str(player.id) + ' has to choose from ' + str(len(legalMoves)) + ' legal moves')
            move = player.playTurn(turn, self.board, legalMoves, self.playerCount)
            print('Played ' + str(move))
            
            if move is None :
                print('Player ' + str(player.id) + ' STOPPED!!!!!')
                player.status = 'STOPPED'
            else:
                self.updateBoard(player,move)
                player.score += move.shape.cellCount
            
            # For next turn
            turn += 1
            currPlayerId = self.getNextPlayer(currPlayerId)
            
            print(self.board.transpose())
        
        # When game ends
        self.status = 'END'
        return self.players
            
    def getNextPlayer(self, currPlayer) :
        if all(p.status == 'STOPPED' for p in self.players):
            return None
        
        i = 1
        while True :
            next = (currPlayer + i) % self.playerCount
            if self.players[next].status == 'PLAYING':
                return next
            i += 1
    
    @staticmethod
    def computeLegalMoves(board, turn, player):
        firstTurn = False
        if (turn in [1,2]) or (turn == 3 and player.id == 2) or (turn == 4 and player.id == 3):
            firstTurn = True
        
        # Get legal cells
        legalCells = Game.legalCells(board,player,firstTurn)
        print('Player ' + str(player.id) + ' has legal cells ' + str(legalCells))
        
        # generate all moves
        allMoves = list()
        for legalCell in legalCells:
            for shape in player.shapes :
                for flip in [0,1]:
                    for rotate in [0,1,2,3]:
                        for connectedValue in range(1,shape.cellCount+1):
                            allMoves.append(
                                Move(
                                    shape,flip, rotate, connectedValue, (legalCell[0],legalCell[1])
                                    )
                                )
                
        #keep only legal moves
        legalMoves = list()
        for move in allMoves :
            if Game.isLegalMove(board, player, move):
                legalMoves.append(move)
        
        return legalMoves

    def updateBoard(self, player, move):
        touchedCells = move.touchedCells
        print('Player ' + str(player.id) + ' will fill cells ' + str(touchedCells))
        for cell in touchedCells:
            self.board[cell[0]][cell[1]] = str(player.id)
    
    @staticmethod
    def legalCells(board,player, firstTurn):
        if firstTurn:
            if player.id==0 : return [(0,0)]
            if player.id==1 : return [(12,12)]
            if player.id==2 : return [(0,12)]
            if player.id==3 : return [(12,0)]
                    
        legalCells = list()
        # Figure out all authorized board cells for player
        for i in range(13):
            for j in range(13):
                if(board[i][j] == '.'):
                    corners = Game.corners(board,i,j)
                    if str(player.id) in corners:
                        sides = Game.sides(board,i,j)
                        if str(player.id) not in sides:
                            legalCells.append((i,j))
        
        return legalCells


    @staticmethod
    def isLegalMove(board,player,move):
        touchedCells = move.touchedCells
        for cell in touchedCells:
            if cell[0] <0 or cell[0] > 12 or cell[1] < 0 or cell[1] > 12 : return False
            if board[cell[0]][cell[1]] != '.' : return False
            sides = Game.sides(board,cell[0], cell[1])
            if str(player.id) in sides: return False
        
        return True
            
    
    @staticmethod
    def sides(board, i, j):
        sides = [(i,j-1),(i,j+1),(i-1,j),(i+1,j)]
        sides = filter(lambda x: x[0] >= 0 and x[0] < 13 and x[1] >= 0 and x[1] < 13, sides)
        sides = map(lambda x : board[x[0]][x[1]],sides)
        return sides
    
    @staticmethod
    def corners(board, i, j):
        corners = [(i-1,j-1),(i+1,j-1),(i-1,j+1),(i+1,j+1)]
        corners = filter(lambda x: x[0] >= 0 and x[0] < 13 and x[1] >= 0 and x[1] < 13, corners)
        corners = map(lambda x : board[x[0]][x[1]],corners)
        return corners    
    
#%%
"""
N = 4
strategies = [Strategy.createRandomStrategy(i) for i in range(N)]
game = Game(N,strategies)

players = game.start()
print(['P' + str(p.id) + ':' + str(p.score) for p in players])
"""
#%%