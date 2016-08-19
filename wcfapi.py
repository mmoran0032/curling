''' wcfapi.py -- Access results database through official means

    The World Curling Federation maintains a results database that can be
    accessed through normal REST means, but requires you to login and append
    your credentials to every request. To ease this, here is a way to access
    the databse through official channels.
'''


import json

import requests


class WCF:
    def __init__(self):
        self.base = r'http://resultsapi.azurewebsites.net/api/'

    def load_user(self):
        with open('credentials.json', 'r') as f:
            self.credentials = json.load(f)
        return self  # to chain load_user().connect()

    def connect(self):
        r = requests.post('{}Authorize'.format(self.base),
                          data=self.credentials)
        assert r.status_code == 200
        self.token = r.text.replace('"', '')
