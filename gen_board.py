import random as rnd
from collections import deque
import itertools as it
import numpy as np
from operator import add

class MyBoard:
    def __init__(self):
        self.squares = [[deque() for _ in range(6)] for x in range(6)]
        self.white_duke = []
        self.black_duke = []

class Piece:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.actions_flipped = []
        self.flipped = 0
        self.coordinates = None
    def __repr__(self):
        return self.name+"_tile"

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
            white_bag.append(Piece(stripped))
            black_bag.append(Piece(stripped))
            flipped = 0
            continue
        
        if stripped == 'FLIP':
            flipped = 1
            continue
        
        ints = [int(item) for item in stripped.split()]
        move = ints
        
        if flipped == 1:
            white_bag[-1].actions_flipped.append(move)
            black_bag[-1].actions_flipped.append(move)
        else:
            white_bag[-1].actions.append(move)
            black_bag[-1].actions.append(move)

board = SetupBoard(white_bag, black_bag)


