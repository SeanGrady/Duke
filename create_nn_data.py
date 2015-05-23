import cPickle as pickle
import gzip
import copy
from collections import deque
import itertools as it
import numpy as np

'''
To avoid being that guy who hardcodes random numbers with no explanation, nn_state is
1259 entries because each state has three parts: the board, and two bags. The board is
36 squares, each of which can have one of the 34 pieces in it (counting white and black
as separate pieces). Each bag can also have one of the 21 pieces in it. Additionally,
there's one neuron representing who's turn it is (1 for white, -1 for black). So,
36*34 + 21 + 21 + 1 = 1267

Also of note, for each input neuron, the input will be 1 for a white piece, 0
for no piece and -1 for a black piece.

IMPORTANT NOTE: I'm hardcoding the fact that there are multiple footmen (ID 0) and pikemen
(ID 5). This is bad and needs to be changed because it means changing things like names.txt
will break this code. 
'''

with open('piece_names.txt') as infile:
    names = [line.strip() for line in infile]

with gzip.open('saved_game.txt.gz', 'rb') as save:
    statelist = pickle.load(save)

nn_statelist = []

'''
save_names_dict = {}
load_names_dict = {}
for i in range(len(names)):
    load_names_dict[i] = names[i]
    save_names_dict[names[i]] = i
'''


num_pieces = 17             #number of unique pieces
num_pieces_tot = 21         #number of pieces total (i.e. there are three footmen, etc)
board_width = 6
board_height = 6
num_neurons = 1267

for state in statelist:
    nn_state = [0]*num_neurons
    board = state[0]
    white_bag = state[1]
    black_bag = state[2]
    turn = state[3] 
    for i in range(board_height):
        for j in range(board_width):
            piece = board[i][j]
            #print piece
            if piece:
                name = piece[0]
                color = piece[1]
                flipped = piece[2]
                square = (i * board_width) + j
                neuron = (num_pieces * 2 * square) + (num_pieces * color) + name
                nn_state[neuron] = (flipped * 2) - 1        #maps (0, 1) to (-1, 1)
    placeholder = board_width * board_height * (num_pieces * 2)
    #print placeholder
    for piece in white_bag:
        neuron = placeholder + piece
        if piece == 0 or piece == 5:
            print "found a thing"
            for i in range(3):
                print neuron, nn_state[neuron]              #This is so bad Ryan don't look :(
                if nn_state[neuron] == 1:
                    neuron += 1
                    continue
                break
        nn_state[neuron] = 1
    placeholder = placeholder + num_pieces_tot
    #print placeholder
    for piece in black_bag:
        neuron = placeholder + piece
        if piece == 0 or piece == 5:
            for i in range(3):              #Don't look at this either I'm a bad person. pls no jdge.
                if nn_state[neuron] == 1:
                    neuron += 1
                    continue
                break
        nn_state[neuron] = 1
    placeholder = placeholder + num_pieces_tot
    #print placeholder
    nn_state[placeholder] = (turn * 2) - 1
    nn_statelist.append(nn_state)
    break
                
