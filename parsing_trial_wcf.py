#!/usr/bin/env python3
''' parsing_trial_wcf.py -- reimplement parsing_trial.py with wcf code

    Since I have my homebrewed API running relatively well, now's the chance to
    turn my old code into new code by actually using it. This course of action
    will also help guide me in what may or may not be missing from that API,
    and what I would need to include in an analysis package.
'''


import wcf


def determine_end_types(game):
    hammer = game.lsfe
    end_types = []
    for end in zip(*game.ends):
        types, hammer = determine_single_end(end, hammer)
        end_types.append(types)
    return [t for t in zip(*end_types)]


def determine_single_end(end, hammer):
    types = determine_types(end, hammer)
    new_hammer = update_hammer(end)
    new_hammer = new_hammer if new_hammer is not None else hammer
    return types, new_hammer


def determine_types(end, hammer):
    ''' Find curling outcome from a single end.'''
    if end[0] > 0 and hammer == 0:
        return 'score-with-hammer', 'blank'
    elif end[1] > 0 and hammer == 1:
        return 'blank', 'score-with-hammer'
    elif end[0] > 0 and hammer == 1:
        return 'steal', 'blank'
    elif end[1] > 0 and hammer == 0:
        return 'blank', 'steal'
    elif end[0] == end[1] == 0 and hammer == 0:
        return 'blank-with-hammer', 'blank'
    elif end[0] == end[1] == 0 and hammer == 1:
        return 'blank', 'blank-with-hammer'


def update_hammer(end):
    if end[0] > 0:
        return 1
    elif end[1] > 0:
        return 0


def get_aggregate(game, types):
    aggregate = []
    for team_ends, team_types, team in zip(game.ends, types, game.teams):
        data = get_team_aggregate(team_ends, team_types)
        data['team-name'] = team
        data['game-type'] = game.draw
        aggregate.append(data)
    return aggregate


def get_team_aggregate(ends, types):
    assert len(ends) == len(types)
    data = {'blank': 0, 'blank-with-hammer': 0, 'steal': 0,
            'score-with-hammer': 0, 'score-2+-with-hammer': 0,
            'team-name': '', 'total-ends': len(ends),
            'total-score': 0, 'stolen-points': 0}
    for points, type in zip(ends, types):
        data[type] += 1
        data['total-score'] += points
        if type == 'steal':
            data['stolen-points'] += points
        elif type == 'score-with-hammer' and points >= 2:
            data['score-2+-with-hammer'] += 1
    return data


t = wcf.Tournament(555)
t.load_all_games()

t_data = []
for game in t.games:  # TODO: make wcf.Tournament an __iter__
    types = determine_end_types(game)
    meta = get_aggregate(game, types)
    t_data.append(meta)

for game in t_data:
    for team in game:
        print(team)
    print('---')
