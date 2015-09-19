class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "P({}, {})".format(self.x, self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, point):
        return (self.x, self.y) == (point.x, point.y)

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, point):
        return self + -point
