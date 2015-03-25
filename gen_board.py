import random as rnd
from collections import deque
import itertools as it
import numpy as np
from operator import add

class MyBoard:
    def __init__(self):
        self.squares = [[deque() for x in range(6)] for y in range(6)]
        self.width = 6
        self.height = 6
        self.eval_dict = {
            0: self.evalMove,
            1: self.evalJump,
            2: self.evalSlide,
            3: self.evalStrike,
            4: self.evalJumpSlide
            #5: self.evalCommandSquare,
            #6: self.evalDivination,
            #7: self.evalSummon
            #8: self.escape
            #9: self.ransom
        }
        self.white_discard = deque()
        self.black_discard = deque()

    def __repr__(self):
        square_width = 16
        board_width = self.width
        width = square_width*board_width + 7
        boardview = ''
        blank_space = '|'+' '*square_width
        blank_row = blank_space*board_width + '|\n'
        line_row = '-'*width + '\n'
        for row in self.squares:
            boardview += line_row
            boardview += blank_row*3
            for space in row:
                boardview += '|'
                if space:
                    margin = 16 - len(space.__repr__())
                    left_margin = margin/2
                    right_margin = margin - left_margin
                    boardview += ' '*left_margin + space.__repr__() + ' '*right_margin
                else:
                    boardview += ' '*square_width
            boardview += '|\n'
            boardview += blank_row*3
        boardview += line_row
        return boardview

    #given a position, check if it is on the board
    def isPosValid(self, position):
        if position[0] not in range(self.height):
            return 0
        if position[1] not in range(self.width):
            return 0
        return 1

    #given a color and a position, check if there is a peice of the same color at position
    def sameColor(self, position, color):
        tile = self.squares[position[0]][position[1]]
        if tile and tile.color == color:
            return 1
        else:
            return 0    

    #List all the pieces currently on the board.
    #The order of nested list comprehensions in python looks weird, but
    #there's a simple explanation for it. Feel free to ask me if you haven't
    #run into it before.
    def listPieces(self):
        return [tile for row in self.squares for tile in row if tile]

    #given a starting postion, a piece color and a move,
    #return wether it's legal and if it's legal return the destination square 
    def evalMove(self, start, move, color):
        step = move[:2]
        num_steps = move[2]
        position = start
        for i in range(num_steps - 1):
            position = map(add, position, step)
            if not self.isPosValid(position):
                return []
            if self.squares[position[0]][position[1]]:
                return []
        position = map(add, position, step)
        if not self.isPosValid(position):
            return []
        if self.sameColor(position, color):
            return []
        return [(start, position, position)]

    #given a starting postion, a piece color and a jump,
    #return wether it's legal and if it's legal return the destination square
    def evalJump(self, start, move, color):
        destination = map(add, start, move)
        if not self.isPosValid(destination):
            return []
        if self.sameColor(destination, color):
            return []
        return [(start, destination, destination)]

    #given a starting postion, a piece color and a slide,
    #return a list of all legal moves, or an empty list if there are none.
    def evalSlide(self, start, move, color):
        valid_slides = []
        position = map(add, start, move)
        while self.isPosValid(position):
            if self.sameColor(position, color):
                break
            valid_slides.append(position)
            position = map(add, position, move)
        if valid_slides:
            valid_moves = [(start, slide, slide) for slide in valid_slides]
            return valid_moves
        else:
            return []
    
    def evalStrike(self, start, move, color):
        position = map(add, start, move)
        if (not self.sameColor(position, color)) and (self.isPosValid(position)):
            return []
        return [('Strike', position, start)]
    
    def evalJumpSlide(self, start, move, color):
        valid_slides = []
        first_position = map(add, start, move)
        if self.isPosValid(first_position) and not self.sameColor(first_position, color):
            valid_slides.append(first_position)
        position = map(add, first_position, move)
        while self.isPosValid(position):
            if self.sameColor(position, color):
                break
            valid_slides.append(position)
            position = map(add, position, move)
        if valid_slides:
            valid_moves = [(start, slide, slide) for slide in valid_slides]
            return valid_moves
        else:
            return []
    
    def evalCommandSquare(self, start, move, color):
        squares = zip(*[iter(move)] * 2)                #lol wut
        allies = []
        destinations = []
        valid_moves = []
        for square in squares:
            if self.isPosValid(square):
                if self.sameColor(square, color):
                    allies.append(list(square))
                else:
                    destinations.append(list(square))
        valid_moves = [(ally, destination, start) for ally in allies for destination in destinations]
        return valid_moves
    
    def evalDivination(self, start, move, color):
        if color == 'White':
            
    
    #def evalSummon(self, start, move, color):
    
    
    #def evalEscape(self, start, move, color):
    
    
    #def evalRansom(self, start, move, color):
    
    
    def ennumerateActions(self, tile, row, column):
        action_list = tile.actions[tile.flipped]
        start = [row, column]
        valid_moves = []
        for action in action_list:
            valid_moves.extend(self.eval_dict[action[0]](start, action[1:], tile.color))
        return valid_moves
    
    
    def moveTable(self):
        move_list = []
        for i in range(self.height):
            for j in range(self.width):
                tile = self.squares[i][j]
                if tile:
                    actions_list = self.ennumerateActions(tile, i, j)
                    if actions_list:
                        move_list.extend(actions_list)
        return move_list
                        

class Piece:
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.actions = [[],[]]
        self.flipped = 0
    
    def __repr__(self):
        rep = self.color+'_'+self.name
        return rep

#given a black and white bag of peices, pick the first three (assumed duke, footman, footman)
#from each bag and place them on the board in starting positions at random.
def SetupBoard(white_bag, black_bag):
    board = MyBoard()
    white_duke = [0, rnd.randint(0,1)+2]
    black_duke = [5, rnd.randint(0,1)+2]
    board.squares[0][white_duke[1]] = white_bag.popleft()
    board.squares[5][black_duke[1]] = black_bag.popleft()

    wh_ftmn_strt = [[0, 1], [0, -1], [1, 0]]
    bl_ftmn_strt = [[0, 1], [0, -1], [-1, 0]]
    rnd.shuffle(wh_ftmn_strt)
    rnd.shuffle(bl_ftmn_strt)
    wfootman1 = map(add, wh_ftmn_strt.pop(), white_duke)
    wfootman2 = map(add, wh_ftmn_strt.pop(), white_duke)
    bfootman1 = map(add, bl_ftmn_strt.pop(), black_duke)
    bfootman2 = map(add, bl_ftmn_strt.pop(), black_duke)
    board.squares[wfootman1[0]][wfootman1[1]] = white_bag.popleft()
    board.squares[wfootman2[0]][wfootman2[1]] = white_bag.popleft()
    board.squares[bfootman1[0]][bfootman1[1]] = black_bag.popleft()
    board.squares[bfootman2[0]][bfootman2[1]] = black_bag.popleft()

    board.white_bag = white_bag
    board.black_bag = black_bag
    board.discard = deque()

    return board
    

with open('piece_names.txt') as infile:
    names = [line.strip() for line in infile]

white_bag = deque([])
black_bag = deque([])
flipped = 0
with open('piece_moves.txt') as infile:
    for line in infile:
        stripped = line.strip()
        if stripped in names:
            white_bag.append(Piece(stripped, 'White'))
            black_bag.append(Piece(stripped, 'Black'))
            flipped = 0
            continue
        
        if stripped == 'FLIP':
            flipped = 1
            continue
        
        ints = [int(item) for item in stripped.split()]
        move = ints
        black_move = [move[0]]
        black_move.extend([-coord for coord in move[1:3]])
        if len(move) > 3:
            black_move.append(move[3])
        
        white_bag[-1].actions[flipped].append(move)
        black_bag[-1].actions[flipped].append(black_move)

board = SetupBoard(white_bag, black_bag)


