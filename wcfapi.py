''' wcfapi.py -- Access results database through official means

    The World Curling Federation maintains a results database that can be
    accessed through normal REST means, but requires you to login and append
    your credentials to every request. To ease this, here is a way to access
    the databse through official channels.
'''


import requests


class WCF:
    def __init__(self):
        self.base = r'http://resultsapi.azurewebsites.net/api/'

    def load_user(self):
        self.username = ''
        self.password = ''

    def connect(self):
        r = requests.post('{}Authorize'.format(self.base),
                          data={'Username': self.username,
                                'Password': self.password})
        assert r.status_code == 200
        self.token = r.text.replace('"', '')
