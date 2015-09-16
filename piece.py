from collections import defaultdict

class Piece:

    def __init__(self, name, color, sides):
        self.name = name
        self.color = color
        self.sides = sides
        self.current_side = 'front'

    def __repr__(self):
        return "{color} {name} ({current_side})".format(color=self.color, name=self.name, current_side=self.current_side)

    """
    def available_moves(self, x, y):
        destinations = defaultdict(list)
        for move_type, move_list in self.sides[self.current_side].iteritems():
            for move in move_list: 
                xdest = move['x'] + x
                ydest = move['y'] + y
                if xdest in range(6) and ydest in range(6):
                    destinations[move_type].append({'x': xdest, 'y': ydest})
        return dict(destinations)
    """

    def f2(self, move_list):
        destinations = []
        for move in move_list: 
            xdest = move['x'] + self.x
            ydest = move['y'] + self.y
            if xdest in range(6) and ydest in range(6):
                destinations.append({'x': xdest, 'y': ydest})
        

    def f1(self, tuple):
        move_type, move_list = tuple
        destinations = map(f2, move_list)
        return (move_type, destinations)

    def available_moves(self):
        return dict(map(self.f1, self.sides[self.current_side].iteritems()))
