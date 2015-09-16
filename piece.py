import yaml

class Piece:

    pieces = yaml.load(open('yamlpieces.yaml', 'r'))

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
        return move['x'] in range(6) and move['y'] in range(6)

    def add_position(self, move):
        return dict(x=move['x'] + self.x, y=move['y'] + self.y)

    def destinations(self, relative_moves):
        return filter(self.is_on_board, map(self.add_position, relative_moves))

    def available_moves(self):
        return {
                move_type: self.destinations(relative_moves)
                for move_type, relative_moves
                in self.sides[self.current_side].iteritems()
        }
