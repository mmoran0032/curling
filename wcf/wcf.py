''' wcf.py -- pull and convert raw data from the WCF

    Provides an easy way to pull data from the WCF's results page and convert
    the raw HTML information into usable python structures and datatypes. A
    Tournament holds multiple BoxScores, and BoxScores contain the important
    game information (teams, LSFE, final score, etc.).

    Example usage:
        t = Tournament(555)
        t.load_all_games()
        # check winner of the final
        final = t.games[-1]
        winner = final.winner  # 0 or 1
        final.teams[winner]

    TODO:
        processing games as a generator
        adjust pulling and formatting data
        dump/load data from json file
'''


from bs4 import BeautifulSoup
import requests


class Tournament:
    ''' Tournament -- holds all important data for a single WCF tournament

        Data is loaded from the WCF results site, and may be either
        automatically parsed using the methods within BoxScore or after the
        fact. Raw box score data is stored in self.games.
    '''
    def __init__(self, id):
        self.id = id
        self.games = []

    def __str__(self):
        return 'WCF Tournament {} ({})'.format(self.id, len(self.games))

    def __iter__(self):
        for game in self.games:
            yield game

    def __len__(self):
        return len(self.games)

    def load_all_games(self):
        ''' Pulls all data from the default WCF results page and saves each
            game as a BoxScores object in self.games
        '''
        _r = self._load_tourney_data()
        _box_scores = self._load_box_scores(_r)
        self._convert_box_scores(_box_scores)

    def _load_tourney_data(self):
        print('pulling data from results.worldcurling.org...')
        params = {'tournamentId': self.id, 'associationId': 0, 'drawNumber': 0}
        site = r'http://results.worldcurling.org/Championship/DisplayResults'
        r = requests.get(site, params=params)
        assert r.status_code == requests.codes.ok
        return r

    def _load_box_scores(self, r):
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find_all('table', class_='game-table')

    def _convert_box_scores(self, raw_box):
        for game in raw_box:
            game_box = BoxScore(game)
            game_box.extract_data()
            self.games.append(game_box)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        assert new_id == int(new_id)
        assert new_id > 0
        self._id = new_id


class BoxScore:
    ''' BoxScore -- holds all important data for a single game

        Raw data from the WCF is split and parsed into usable values.
    '''
    def __init__(self, raw_box_score):
        self.raw = raw_box_score

    def __str__(self):
        try:
            return '{} {} {}\n{} {} {}\nDraw {}, Sheet {}, LSFE {}'.format(
                self.teams[0], self.ends[0], self.total[0],
                self.teams[1], self.ends[1], self.total[1],
                self.draw, self.sheet, self.teams[self.lsfe]
            )
        except:
            return 'Box Score ({}...)'.format(repr(self.raw)[:20])

    def extract_data(self):
        ''' Converts raw data into correctly-typed attributes.'''
        self._pull_data()
        self._reformat_data()
        self._determine_winner()
        del self.raw

    def _pull_data(self):
        self.draw = self._pull_info('th', 'game-header', single=True)
        self.sheet = self._pull_info('td', 'game-sheet', single=True)
        self.teams = self._pull_info('td', 'game-team')
        self.lsfe = self._pull_info('td', 'game-hammer')
        self.total = self._pull_info('td', 'game-total')
        self.ends = self._pull_info('tr', None)

    def _pull_info(self, tag, class_, single=False):
        if single:
            return self.raw.find(tag, class_=class_)
        else:
            return self.raw.find_all(tag, class_=class_)

    def _reformat_data(self):
        self.draw = self._reformat(self.draw, single=True)
        self.sheet = self._reformat(self.sheet, single=True)
        self.teams = self._reformat(self.teams)
        self.lsfe = self._reformat_lsfe()
        self.total = self._reformat(self.total, convert=int)
        self.ends = self._reformat_end_scores()

    def _reformat(self, data, single=False, **kwargs):
        if single:
            return data.text.strip()
        else:
            return self._reformat_group(data, **kwargs)

    def _reformat_lsfe(self):
        lsfe = self._reformat_group(self.lsfe)
        return lsfe.index('*')

    def _reformat_end_scores(self):
        new_ends = []
        for row in self.ends:
            scores = row.find_all('td', 'game-end10')
            scores = self._reformat_group(
                scores, convert=int, remove='X')
            new_ends.append(scores)
        return new_ends

    def _reformat_group(self, data, convert=None, remove=None):
        data = [d.text.strip() for d in data]
        if remove:
            data = [d.replace(remove, '') for d in data]
        if convert:
            data = [convert(d) for d in data if d]
        return data

    def _determine_winner(self):
        self.winner = self.total.index(max(self.total))
