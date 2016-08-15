#!/usr/bin/env python3


import unittest

from bs4 import BeautifulSoup

from wcf import BoxScore

with open('./tests/test_game.html', 'r') as f:
    test_game_text = f.read()
test_game = BeautifulSoup(test_game_text, 'html.parser')


class TestBoxScore(unittest.TestCase):
    def setUp(self):
        self.b = BoxScore(test_game)

    def test_game_loaded(self):
        self.assertNotEqual(len(str(self.b)), 0)


if __name__ == '__main__':
    unittest.main()
