import game

import unittest
from unittest.mock import patch


class GameTests(unittest.TestCase):
    @patch('game.load_image')
    def test_load_completed(self, test_patch):
        path = game.load_image('sprites/blocks/blue_block.png')
        self.assertEqual(path, 'data/sprites/blocks/blue_block.png')

    def test_load_failed(self):
        pass


if __name__ == '__name__':
    unittest.main()
