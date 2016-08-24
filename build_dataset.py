#!/usr/bin/env python3


import wcf

from analyze import determine_end_types, get_aggregate


def create_line(game):
    t1data, t2data = game
    if t1data['game-type'].startswith('Draw'):
        winner, loser = (t1data, t2data) if t1data['won'] else (t2data, t1data)
        l = line.format(tournament_id, 2016,
                        winner['team-name'], winner['total-score'],
                        loser['team-name'], loser['total-score'],
                        winner['total-ends'])
        return l


tournament_id = 555
t = wcf.Tournament(tournament_id)
t.load_all_games()

t_data = []
for game in t:
    types = determine_end_types(game)
    meta = get_aggregate(game, types)
    t_data.append(meta)

# build basic data
header = '#tID,year,wteam,wscore,lteam,lscore,ends\n'
line = '{},{},{},{},{},{},{}'
lines = [create_line(g) for g in t_data]
lines = [l for l in lines if l is not None]

with open('data/555_basic_roundrobin.csv', 'w') as f:
    f.write(header)
    f.write('\n'.join(lines))
