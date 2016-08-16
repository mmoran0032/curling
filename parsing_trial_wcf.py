#!/usr/bin/env python3
''' parsing_trial_wcf.py -- reimplement parsing_trial.py with wcf code

    Since I have my homebrewed API running relatively well, now's the chance to
    turn my old code into new code by actually using it. This course of action
    will also help guide me in what may or may not be missing from that API,
    and what I would need to include in an analysis package.
'''


import wcf


def determine_end_types(game):
    current_hammer = game.lsfe.index(True)
    for end in zip(*game.ends):
        pass


def get_aggregate(game):
    pass


t = wcf.Tournament(555)
t.load_all_games()

for game in t.games:  # TODO: make wcf.Tournament an __iter__
    pass
