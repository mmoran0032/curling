#!/usr/bin/env python3


from collections import namedtuple
import json
import os


fields = ['TournamentId', 'GameId', 'date', 'gametype', 'team1', 'team2',
          'LSFE', 't1_total', 't2_total', 'total_ends']
Game = namedtuple('WCF_Game', fields)


def pull_basic_data(game):
    id = game['Id']
    date = game['DrawInfo']['GameStart'][:10]
    tournament = game['TournamentId']
    lsfe = game['TossWinner']
    draw = game['Round']['Name']
    teams = (game['Team1']['Team']['Code'], game['Team2']['Team']['Code'])
    return (tournament, date, id, draw, *teams, lsfe)


def pull_end_data(ends):
    end_data = [(end['Team1'], end['Team2']) for end in ends]
    return end_data


data_directory = 'data/raw'
output_directory = 'data/processed'

files = []
for filename in sorted(os.listdir(data_directory)):
    number = filename.split('.')[0]
    filename = '{}/{}'.format(data_directory, filename)
    print(filename)
    with open(filename, 'r') as f:
        data = json.load(f)

    game_data = []
    for game in data:
        try:
            basic = pull_basic_data(game)
            ends = pull_end_data(game['Ends'])
            ends = list(zip(*ends))
            scores = [sum(ends[0]), sum(ends[1])]
            g = Game(basic[0], basic[2], basic[1], basic[3], basic[4],
                     basic[5], basic[6], scores[0], scores[1], len(ends[0]))
            game_data.append(g)
        except:
            print('  tournament not structured properly')
            del game_data
            break

    outfile = '{}/{}_basic.csv'.format(output_directory, number)
    try:
        with open(outfile, 'w') as f:
            f.write('tournamentid,gameid,date,draw,team1,team2')
            f.write(',lsfe,t1score,t2score,ends\n')
            for game in game_data:
                f.write(','.join(str(i) for i in game))
                f.write('\n')
    except:
        print('  writing failed')
        os.remove(outfile)
