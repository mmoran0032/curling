#!/usr/bin/env python3
''' parsing_trial.py -- turn tourney raw data into something meaningful

    Now that I can reliably access all of the required data from the WCF's
    website, I now need to convert that into something usable. This means that
    instead of storing individual end scores, you want things like hammer
    conversion rates and percentage of blanked ends.
'''


import re

from bs4 import BeautifulSoup
import requests


def reformat_data(data, converter=None):
    data = [d.text.strip() for d in data]
    if converter:
        data = [d.replace('X', '') for d in data]
        data = [converter(d) for d in data if d is not '']
    return data


def pull_end_scores(game):
    rows = game.find_all('tr', class_=None)
    end_scores = []
    for row in rows:
        scores = row.find_all('td', class_='game-end10')
        scores = reformat_data(scores, converter=int)
        end_scores.append(scores)
    return end_scores


def determine_end_types(t0_score, t1_score, hammer_team):
    # regular scoring
    if t0_score > 0 and hammer_team == 0:
        return 'score-with-hammer', 'blank'
    elif t1_score > 0 and hammer_team == 1:
        return 'blank', 'score-with-hammer'
    # steals
    elif t0_score > 0 and hammer_team == 1:
        return 'steal', 'blank'
    elif t1_score > 0 and hammer_team == 0:
        return 'blank', 'steal'
    # blanks
    elif t0_score == 0 and t1_score == 0 and hammer_team == 0:
        return 'blank-with-hammer', 'blank'
    elif t0_score == 0 and t1_score == 0 and hammer_team == 1:
        return 'blank', 'blank-with-hammer'


def get_aggregate(team_data):
    data = {'blank': 0, 'blank-with-hammer': 0, 'steal': 0,
            'score-with-hammer': 0, 'score-2+-with-hammer': 0,
            'team-name': team_data[0], 'total-ends': len(team_data) - 1,
            'total-score': 0, 'stolen-points': 0}
    ends = team_data[1:]
    for end in ends:
        data[end[1]] += 1
        data['total-score'] += end[0]
        if end[1] == 'score-with-hammer' and end[0] > 1:
            data['score-2+-with-hammer'] += 1
        if end[1] == 'steal':
            data['stolen-points'] += end[0]
    return data


name = re.compile('[\w\s]+')
params = {'tournamentId': 555, 'associationId': 0, 'drawNumber': 0}
results_site = r'http://results.worldcurling.org/Championship/DisplayResults'

r = requests.get(results_site, params=params)
assert r.status_code == 200
soup = BeautifulSoup(r.text, 'html.parser')
box_scores = soup.find_all('table', class_='game-table')

tourney_data = []

for game in box_scores:
    draw = game.find('th', class_='game-header').text.strip()
    sheet = game.find('td', class_='game-sheet').text.strip()
    teams = [t for t in game.find_all('td', class_='game-team')]
    teams = reformat_data(teams)
    hammer = [h for h in game.find_all('td', class_='game-hammer')]
    hammer = reformat_data(hammer)
    final_score = [s for s in game.find_all('td', class_='game-total')]
    final_score = reformat_data(final_score, converter=int)
    end_scores = pull_end_scores(game)
    end_scoresT = [[s1, s2] for s1, s2 in zip(*end_scores)]

    t0_data = [teams[0]]
    t1_data = [teams[1]]
    hammer_team = hammer.index('*')
    for score in end_scoresT:
        t0_score, t1_score = score
        t0_type, t1_type = determine_end_types(*score, hammer_team)
        t0_end, t1_end = [t0_score, t0_type], [t1_score, t1_type]
        t0_data.append(t0_end)
        t1_data.append(t1_end)

        if t0_score > 0:
            hammer_team = 1
        elif t1_score > 0:
            hammer_team = 0

    t0_agg = get_aggregate(t0_data)
    t1_agg = get_aggregate(t1_data)
    t0_agg['game-type'] = draw
    t1_agg['game-type'] = draw

    # need to remember to mark who won the game...
    t0_agg['won'] = True if final_score[0] > final_score[1] else False
    t1_agg['won'] = True if final_score[1] > final_score[0] else False

    tourney_data.append([t0_agg, t1_agg])

for game in tourney_data:
    for team in game:
        print(team)
    print('---')

for game in tourney_data:
    print(game[0]['game-type'], game[1]['game-type'])
