''' wcfapi.py -- Access results database through official means

    The World Curling Federation maintains a results database that can be
    accessed through normal REST means, but requires you to login and append
    your credentials to every request. To ease this, here is a way to access
    the databse through official channels.
'''


import json

import requests


class WCF:
    def __init__(self, timeout=1.0):
        self.base = r'http://resultsapi.azurewebsites.net/api'
        self.timeout = timeout

    def load_user(self):
        with open('credentials.json', 'r') as f:
            self.credentials = json.load(f)
        return self  # to chain load_user().connect()

    def connect(self):
        r = requests.post('{}/Authorize'.format(self.base),
                          data=self.credentials,
                          timeout=self.timeout)
        assert r.status_code == requests.codes.ok
        self.token = r.json()

    def get_people(self, surname=None, details=None):
        surname = surname if surname else 'none'
        details = details if details else 'none'
        r = requests.get('{}/People'.format(self.base),
                         headers={'Authorize': self.token},
                         params={'surname': surname, 'details': details},
                         timeout=self.timeout)
        assert r.status_code == requests.codes.ok
        return r.json()

    def get_draws_by_tournament(self, id):
        r = requests.get('{}/Draws/Tournament/{}'.format(self.base, id),
                         headers={'Authorize': self.token},
                         timeout=self.timeout)
        assert r.status_code == requests.codes.ok
        return r.json()
