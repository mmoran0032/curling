

from bs4 import BeautifulSoup
import requests


class Tournament:
    ''' Tournament - holds all important data for a single WCF tournament

        Data is loaded from the WCF results site, and may be either
        automatically parsed using the methods within BoxScore or after the
        fact. Raw box score data is stored in self.box_scores.
    '''
    def __init__(self, id):
        self.id = id
        self.box_scores = []

    def __str__(self):
        return 'WCF Tournament {} ({})'.format(self.id, len(self.box_scores))

    def load_all_games(self):
        ''' Pulls all data from the default WCF results page and saves each
            game as a BoxScores object in self.box_scores
        '''
        _r = self._load_tourney_data()
        _box_scores = self._load_box_scores(_r)
        self._convert_box_scores(_box_scores)

    def _load_tourney_data(self):
        params = {'tournamentId': self.id, 'associationId': 0, 'drawNumber': 0}
        site = r'http://results.worldcurling.org/Championship/DisplayResults'
        r = requests.get(site, params=params)
        assert r.status_code == 200
        return r

    def _load_box_scores(self, r):
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find_all('table', class_='game-table')

    def _convert_box_scores(self, raw_box):
        for game in raw_box:
            game_box = BoxScore(game)
            game_box.extract_data()
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
    ''' BoxScore - holds all important data for a single game

        Raw data from the WCF is split and parsed into usable values.
    '''
    def __init__(self, raw_box_score):
        self.raw = raw_box_score
        self.ends = []

    def __str__(self):
        try:
            return '{} {} {} {}\n{} {} {} {}\nDraw {} Sheet {}'.format(
                self.teams[0], self.hammer[0], self.ends[0], self.final[0],
                self.teams[1], self.hammer[1], self.ends[1], self.final[1],
                self.draw, self.sheet
            )
        except:
            return 'Box Score {}'.format(repr(self.raw))

    def extract_data(self):
        ''' Converts raw data into correctly-typed attributes.'''
        self._pull_basic_data()
        self._pull_end_scores()
        self.winner = self.final.index(max(self.final))

    def _pull_basic_data(self):
        self.draw = self.raw.find('th', class_='game-header').text.strip()
        self.sheet = self.raw.find('td', class_='game-sheet').text.strip()
        self.teams = self._pull_and_reformat(self.raw, 'game-team')
        self.hammer = self._pull_and_reformat(self.raw, 'game-hammer')
        self.final = self._pull_and_reformat(self.raw, 'game-total', int)

    def _pull_end_scores(self):
        rows = self.raw.find_all('tr', class_=None)
        for row in rows:
            scores = self._pull_and_reformat(
                row, 'game-end10', converter=int, remove='X')
            self.ends.append(scores)

    def _pull_and_reformat(self, raw, class_, converter=None, remove=None):
        data = raw.find_all('td', class_=class_)
        data = [d.text.strip() for d in data]
        if remove:
            data = [d.replace(remove, '') for d in data]
        if converter:
            data = [converter(d) for d in data if d is not '']
        return data
