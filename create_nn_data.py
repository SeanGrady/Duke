import cPickle as pickle
import gzip
import copy
from collections import deque
import itertools as it
import numpy as np

'''
To avoid being that guy who hardcodes random numbers with no explanation, nn_state is
647 entries because each state has three parts: the board, and two bags. The board is
36 squares, each of which can have one of the 17 pieces in it. Each bag can also have one
of the 17 pieces in it. Additionally, there's one neuron representing who's turn it is (1
for white, -1 for black). So, 36*17 + 17 + 17 + 1 = 647

Also of note, for each input neuron, the input will be 1 for a white piece, 0
for no piece and -1 for a black piece.
'''

with open('piece_names.txt') as infile:
    names = [line.strip() for line in infile]

with gzip.open('saved_game.txt.gz', 'rb') as save:
    statelist = pickle.load(save)

nn_statelist = []


'''
for state in statelist:
    nn_state = [0]*647 
    for container in statelist:    
'''
