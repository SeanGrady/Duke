import yaml
from pprint import pprint
from piece import Piece

PIECES_FILENAME = 'yamlpieces.yaml'

board = [[None]*6 for _ in range(6)]
pieces = yaml.load(open(PIECES_FILENAME, 'r'))
footman = Piece('Footman', 'white', pieces['Footman'])
bowman = Piece('Bowman', 'white', pieces['Bowman'])
bowman.current_side = 'back'
x = y = 4
bowman.x = x
bowman.y = y
#board[x][y] = footman
board[x][y] = bowman

pprint(board)
pprint(bowman.available_moves())
