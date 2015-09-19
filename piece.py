import yaml
import os
from settings import APP_ROOT
from point import Point

class PieceHelper:

    @staticmethod
    def alter_moves_list(func, side):
        return {
                move_type: set(func(relative_moves))
                for move_type, relative_moves
                in side.iteritems()
        }

    @staticmethod
    def enpointen(moves_list):
        return [Point(**move) for move in moves_list]
        #return map(Point, moves_list)

    @classmethod
    def load_pieces(cls):
        pieces = yaml.load(open(os.path.join(APP_ROOT, 'yamlpieces.yaml'), 'r'))
        for piece, sides in pieces.iteritems():
            for side_name, side in sides.iteritems():
                pieces[piece][side_name] = cls.alter_moves_list(
                        cls.enpointen,
                        side,
                )

        return pieces

class Piece:

    pieces = PieceHelper.load_pieces()

    def __init__(self, name, color, current_side=None, x=None, y=None):
        self.name = name
        self.color = color
        self.current_side = current_side
        self.x = x
        self.y = y
        self.sides = self.pieces[self.name.capitalize()]

    def __repr__(self):
        return "{color} {name} ({current_side})".format(
                color=self.color,
                name=self.name,
                current_side=self.current_side
        )

    def is_on_board(self, move):
        return move.x in range(6) and move.y in range(6)

    def add_position(self, move):
        return Point(self.x, self.y) + move

    def destinations(self, relative_moves):
        return filter(self.is_on_board, map(self.add_position, relative_moves))

    def available_moves(self):
        return PieceHelper.alter_moves_list(
                self.destinations,
                self.sides[self.current_side],
        )
