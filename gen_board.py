import random as rnd
from collections import deque
import itertools as it
import numpy as np
from operator import add

class MyBoard:
    def __init__(self):
        self.squares = [[deque() for x in range(6)] for y in range(6)]

    def __repr__(self):
        square_width = 16
        board_width = 6
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
                    margin = 16 - len(space.name)
                    left_margin = margin/2
                    right_margin = margin - left_margin
                    boardview += ' '*left_margin + space.name + ' '*right_margin
                else:
                    boardview += ' '*square_width
            boardview += '|\n'
            boardview += blank_row*3
        boardview += line_row
        return boardview
    
    def listPieces(self):
        return [tile for row in board.squares for tile in row if tile]
    '''
    def moveTable(self):
        for peice in listPieces():
    '''        

class Piece:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.actions_flipped = []
        self.flipped = 0
    
    def __repr__(self):
        return self.name

#Need to make the starting positions truly random instead of picking between two
def SetupBoard(white_bag, black_bag):
    board = MyBoard()
    white_duke = [0, rnd.randint(0,1)+2]
    black_duke = [5, rnd.randint(0,1)+2]
    board.squares[0][white_duke[1]] = white_bag.popleft()
    board.squares[5][black_duke[1]] = black_bag.popleft()

    wfootman1 = map(add, [0, -1], white_duke)
    wfootman2 = map(add, [0, 1], white_duke)
    bfootman1 = map(add, [0, -1], black_duke)
    bfootman2 = map(add, [0, 1], black_duke)
    board.squares[0][wfootman1[1]] = white_bag.popleft()
    board.squares[0][wfootman2[1]] = white_bag.popleft()
    board.squares[5][bfootman1[1]] = black_bag.popleft()
    board.squares[5][bfootman2[1]] = black_bag.popleft()

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
            white_bag.append(Piece('White_'+stripped))
            black_bag.append(Piece('Black_'+stripped))
            flipped = 0
            continue
        
        if stripped == 'FLIP':
            flipped = 1
            continue
        
        ints = [int(item) for item in stripped.split()]
        move = ints
        black_move = [move[0]]
        black_move.append([-coord for coord in move[1:]])
        
        if flipped == 1:
            white_bag[-1].actions_flipped.append(move)
            black_bag[-1].actions_flipped.append(black_move)
        else:
            white_bag[-1].actions.append(move)
            black_bag[-1].actions.append(black_move)

board = SetupBoard(white_bag, black_bag)


