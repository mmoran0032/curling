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


name = re.compile('[\w\s]+')
params = {'tournamentId': 555, 'associationId': 0, 'drawNumber': 0}
results_site = r'http://results.worldcurling.org/Championship/DisplayResults'
