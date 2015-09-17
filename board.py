class Board:

    def __init__(self):
        self.xsize = 6
        self.ysize = 6
        self.board = [[None]*self.ysize for _ in range(self.xsize)]

    def put(self, x, y, piece):
        self.board[x][y] = piece

    def get(self, x, y):
        return self.board[x][y]

    def search(self, piece_name):
        raise Exception('not implemented')
