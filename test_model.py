import unittest
from unittest.mock import patch
from model import grid

class TestGrid(unittest.TestCase):
    def setUp(self):
        self.g = grid()

    def test_counts(self):
        w, b = self.g.get_counts()
        self.assertEqual(w, 7)
        self.assertEqual(b, 7)

    def test_get_pos_existing(self):
        pos = self.g.get_pos('1W')
        self.assertIsNotNone(pos)
        x,y = pos
        self.assertEqual(self.g.grid[x,y], '1W')

    def test_get_roll_range(self):
        with patch('random.randint', return_value=3):
            self.assertEqual(self.g.get_roll(), 3)

    def test_move_piece_success(self):
        # move 1W by 3 -> from index 0 to index 3
        with patch.object(self.g, 'get_roll', return_value=3):
            old_pos = self.g.get_pos('1W')
            self.assertTrue(self.g.move_piece('1W'))
            new_pos = self.g.get_pos('1W')
            self.assertNotEqual(old_pos, new_pos)

    def test_move_off_board(self):
        # force a large roll to push off board
        with patch.object(self.g, 'get_roll', return_value=100):
            result = self.g.move_piece('1W')
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
