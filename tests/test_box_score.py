#!/usr/bin/env


import unittest

from bs4 import BeautifulSoup

from wcf import BoxScore


class TestBoxScore(unittest.TestCase):
    def setUp(self):
        b = BoxScore()
