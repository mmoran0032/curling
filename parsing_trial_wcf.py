#!/usr/bin/env python3
''' parsing_trial_wcf.py -- reimplement parsing_trial.py with wcf code

    Since I have my homebrewed API running relatively well, now's the chance to
    turn my old code into new code by actually using it. This course of action
    will also help guide me in what may or may not be missing from that API,
    and what I would need to include in an analysis package.
'''


import wcf

from analyze import determine_end_types, get_aggregate


t = wcf.Tournament(555)
t.load_all_games()

t_data = []
for game in t:
    types = determine_end_types(game)
    meta = get_aggregate(game, types)
    t_data.append(meta)

for game in t_data:
    for team in game:
        print(team)
    print('---')
