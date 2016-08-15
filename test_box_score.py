#!/usr/bin/env python3


import unittest

from bs4 import BeautifulSoup

from wcf import BoxScore


# use the final game from tourney 555 for testing
with open('game.html', 'r') as f:
    test_game_text = f.read()
test_game = BeautifulSoup(test_game_text, 'html.parser')


class TestBoxScore(unittest.TestCase):
    def setUp(self):
        self.b = BoxScore(test_game)

    def test_game_loaded(self):
        self.assertNotEqual(len(str(self.b)), 0)

    def test_pull_single(self):
        h = self.b._pull_info('th', 'game-header', single=True)
        h = h.text.strip()
        self.assertEqual(h, 'Final')

    def test_pull_group(self):
        h = self.b._pull_info('td', 'game-team')
        self.assertEqual(len(h), 2)
        h = [s.text.strip() for s in h]
        self.assertIn('Canada', h)
        self.assertIn('Denmark', h)

    def test_winner(self):
        self.b.extract_data()
        self.assertEqual(self.b.winner, 1)

    def test_end_reformat(self):
        self.b.ends = self.b._pull_info('tr', None)
        self.b.ends = self.b._reformat_end_scores()
        e = self.b.ends
        self.assertEqual(len(e), 2)
        self.assertEqual(len(e[0]), len(e[1]))
        self.assertEqual(len(e[0]), 9)

    def test_reformat_group(self):
        data = self.build_data()
        data = self.b._reformat_group(data)
        self.assertEqual(len(data), 3)
        self.assertIsInstance(data, list)
        self.assertEqual('1', data[0])

    def test_reformat_convert(self):
        data = self.build_data()
        data = self.b._reformat_group(data, convert=int)
        self.assertIsInstance(data[0], int)

    def build_data(self):
        data = BeautifulSoup('<a>1</a><a>2</a><a>3</a>', 'html.parser')
        data = data.find_all('a')
        return data


if __name__ == '__main__':
    unittest.main()
