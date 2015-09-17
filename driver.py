from pprint import pprint
from piece import Piece

board = [[None]*6 for _ in range(6)]
#footman = Piece('Footman', 'white', pieces['Footman'])
x = y = 4
bowman = Piece('Bowman', 'white', current_side='back', x=x, y=y)
#board[x][y] = footman
board[x][y] = bowman

pprint(board)
pprint(bowman.available_moves())
