#!/usr/bin/env python3


import os
import json

from progressbar import ProgressBar

import wcf


db_conn = wcf.WCF(connect=True)

tournaments = db_conn.get_tournaments_by_type(1)  # World Curling Championships
tourney_ids = [t['Id'] for t in tournaments]

print('Pulling game data...')
progress = ProgressBar()
# over WiFi at home, next part takes about a minute
for id in progress(tourney_ids):
    if not os.path.isfile('data/raw/{:03d}.json'.format(id)):
        data = db_conn.get_draws_by_tournament(id)
        with open('data/raw/{:03d}.json'.format(id), 'w') as f:
            json.dump(data, f, indent=2)
