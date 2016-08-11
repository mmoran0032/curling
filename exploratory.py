#!/usr/bin/env python3
''' exploratory.py -- converting ipynb to script

    Since the exploratory work I did in exploratory.ipynb is pretty close to
    done, I have rewritten the important parts in this single script while also
    combining the two separate scraping portions of the box scores.

    Right now, this does not save the data in any form and still just pulls
    from my single test case webpage, but that is not a bad thing. The data is
    pulled in quickly and correctly, and this could easily be expanded to pull
    from an arbitrary tournamentId, associationId, and drawNumber.
'''


import re

from bs4 import BeautifulSoup
import requests


name = re.compile('[\w\s]+')
params = {'tournamentId': 555, 'associationId': 0, 'drawNumber': 0}
results_site = r'http://results.worldcurling.org/Championship/DisplayResults'

r = requests.get(results_site, params=params)
assert r.status_code == 200
soup = BeautifulSoup(r.text, 'html.parser')

box_scores = soup.find_all('table', class_='game-table')
for i, box_score in enumerate(box_scores):
    print('=== GAME {} ==='.format(i + 1))
    for row in box_score.find_all('tr'):
        sheet, team_name, hammer, scores = None, None, None, None
        sheet = row.find('td', class_='game-sheet')
        team = row.find('td', class_='game-team')
        hammer = row.find('td', class_='game-hammer')
        scores = row.find_all('td', class_='game-end10')
        if sheet is not None:
            sheet = sheet.text.strip()
        if team is not None:
            team_name = re.search(name, team.text.strip()).group(0)
        if scores is not None:
            scores = [end.text.strip().replace('X', '') for end in scores]
            scores = [int(end) for end in scores if end.isdigit()]
        if hammer is not None:
            hammer = hammer.text.strip()
            if hammer == '*':
                hammer = True
            else:
                hammer = False

            print('Team: {}, LSFE: {}, scores: {}, total: {}'.format(
                team_name, hammer, scores, sum(scores)
            ))
    print()
