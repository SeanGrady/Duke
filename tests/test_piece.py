from piece import Piece
from point import Point
import unittest

class TestPiece(unittest.TestCase):

    def test_bowman(self):
        x = y = 4
        bowman = Piece('Bowman', 'white', current_side='back', x=x, y=y)

        expected_moves = {
                'strike': set([Point(5, 5), Point(5, 3)]),
                'move': set([Point(5, 4), Point(3, 5), Point(3, 3)]),
        }
        self.assertEqual(bowman.available_moves(), expected_moves)

    def test_footman(self):
        x = y = 3
        footman = Piece('Footman', 'white', current_side='front', x=x, y=y)

        expected_moves = {
                'move': set([
                    Point(2, 3), Point(4, 3),
                    Point(3, 2), Point(3, 4),
                ]),
        }
        self.assertEqual(footman.available_moves(), expected_moves)

if __name__ == "__main__":
    unittest.main()
