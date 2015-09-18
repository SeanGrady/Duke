from point import Point
import unittest

class TestPoint(unittest.TestCase):

    def test_add(self):
        a = Point(3, 5)
        b = Point(2, 1)
        self.assertEqual(Point(5, 6), a + b)

    def test_sub(self):
        a = Point(3,2)
        b = Point(2,3)
        self.assertEqual(Point(1, -1), a - b)

    def test_dict(self):
        a = Point(3, 5)
        b = Point(2, 4)
        d = {a: "This is point a.", b: "This is point b."}
        print d
        self.assertEqual(d[a], "This is point a.")

if __name__ == "__main__":
    unittest.main()

