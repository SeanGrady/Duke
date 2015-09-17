from piece import Piece
import unittest

class TestPiece(unittest.TestCase):

    def test_bowman(self):
        x = y = 4
        bowman = Piece('Bowman', 'white', current_side='back', x=x, y=y)

        expected_moves = {
                'strike': [{'x': 5, 'y': 5}, {'x': 5, 'y': 3}],
                'move': [{'x': 5, 'y': 4}, {'x': 3, 'y': 5}, {'x': 3, 'y': 3}],
        }
        self.assertEqual(bowman.available_moves(), expected_moves)

    def test_footman(self):
        x = y = 3
        footman = Piece('Footman', 'white', current_side='front', x=x, y=y)

        expected_moves = {
                'move': [
                    {'x': 2, 'y': 3}, {'x': 4, 'y': 3},
                    {'x': 3, 'y': 2}, {'x': 3, 'y': 4},
                ],
        }
        self.assertEqual(footman.available_moves(), expected_moves)

if __name__ == "__main__":
    unittest.main()
