''' analyze.py -- helper functions for curling analysis

    Instead of copying over the functions I need every time, here's a small
    suite of functions to pull out the important data from the box scores.
'''


def determine_end_types(game):
    hammer = game.lsfe
    end_types = []
    for end in zip(*game.ends):
        types, hammer = _determine_single_end(end, hammer)
        end_types.append(types)
    return [t for t in zip(*end_types)]


def _determine_single_end(end, hammer):
    types = _determine_types(end, hammer)
    new_hammer = _update_hammer(end)
    new_hammer = new_hammer if new_hammer is not None else hammer
    return types, new_hammer


def _determine_types(end, hammer):
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


def _update_hammer(end):
    if end[0] > 0:
        return 1
    elif end[1] > 0:
        return 0


def get_aggregate(game, types):
    aggregate = []
    for team_ends, team_types, team in zip(game.ends, types, game.teams):
        data = _get_team_aggregate(team_ends, team_types)
        data['team-name'] = team
        data['game-type'] = game.draw
        aggregate.append(data)
    aggregate[game.winner]['won'] = True
    return aggregate


def _get_team_aggregate(ends, types):
    ''' Builds a dict with "meta-data" about the game for a single team.'''
    assert len(ends) == len(types)
    data = {'blank': 0, 'blank-with-hammer': 0, 'steal': 0,
            'score-with-hammer': 0, 'score-2+-with-hammer': 0,
            'team-name': '', 'total-ends': len(ends),
            'total-score': 0, 'stolen-points': 0, 'won': False}
    for points, type in zip(ends, types):
        data['total-score'] += points
        data[type] += 1
        if type == 'steal':
            data['stolen-points'] += points
        elif type == 'score-with-hammer' and points >= 2:
            data['score-2+-with-hammer'] += 1
    return data
