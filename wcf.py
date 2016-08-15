

from bs4 import BeautifulSoup
import requests


class Tournament:
    def __init__(self, id):
        self.id = id
        self.site = r'http://results.worldcurling.org/Championship/DisplayResults'

    def load_all_games(self):
        _r = self._load_tourney_data()
        _box_scores = self._load_box_scores(_r)
        self._convert_box_scores(_box_scores)

    def _load_tourney_data(self):
        params = {'tournamentId': self.id, 'associationId': 0, 'drawNumber': 0}
        r = requests.get(self.site, params=params)
        assert r.status_code == 200
        return r

    def _load_box_scores(self, r):
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find_all('table', class_='game-table')

    def _convert_box_scores(self, raw_box):
        self.box_scores = []
        for game in raw_box:
            game_box = BoxScore(game)
            self.box_scores.append(game_box)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        assert new_id == int(new_id)
        assert new_id > 0
        self._id = new_id


class BoxScore:
    def __init__(self, raw_box_score):
        pass
