from pprint import pprint
from piece import Piece

#footman = Piece('Footman', 'white', pieces['Footman'])
x = y = 4
bowman = Piece('Bowman', 'white', current_side='back', x=x, y=y)

#pprint(Piece.pieces['Bowman'])
actual = bowman.available_moves()
expected = {
        'move': [{'x': 5, 'y': 4}, {'x': 3, 'y': 5}, {'x': 3, 'y': 3}],
        'strike': [{'x': 5, 'y': 5}, {'x': 5, 'y': 3}],
}
if actual == expected:
    print 'pass'
else:
    print 'fail'
