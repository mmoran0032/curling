#!/usr/bin/env python3


import json
from pathlib import Path

import wcf


print(f'WCF API version {wcf.__version__}')
conn = wcf.API('../credentials/wcf.json', timeout=15).connect()

# NOTE: IDs before 190 may not be reliable
print('Getting tournament IDs')
tournaments = conn.get_tournaments_by_type(1)  # World Curling Championships
# tournaments = conn.get_tournaments_by_type(4)  # Olympic Games
tourney_ids = [t['Id'] for t in tournaments]
print(len(tourney_ids))

# over WiFi at home, next part takes about a minute
for id_ in tourney_ids:
    path = Path(f'data/raw/{id_:03d}.json')
    if not path.is_file():
        print(f'  Saving Tournament {id_}')
        data = conn.get_draws_by_tournament(id_)
        with path.open('w') as f:
            json.dump(data, f, indent=2)
