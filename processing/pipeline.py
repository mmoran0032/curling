''' pipeline -- process WCF data
'''


import pandas as pd


game_fields = [
    'tourney_id', 'game_id', 'round', 'team_0', 'team_1',
    'end_number', 'hammer', 'scored_points', 'scoring_team'
]
state_fields = [
    'score_diff', 'score_ends_diff',
    'score_hammer_diff', 'score_hammer_ends_diff',
    'steal_diff', 'steal_ends_diff',
    'blanks'
]
fields = [*game_fields, *state_fields, 'winning_team']


def convert(games):
    data = []
    for game in games:
        single = convert_single(game)
        data.extend(single)
    return pd.DataFrame(data=data, columns=fields)


def convert_single(game):
    cur_state = [0, 0, 0, 0, 0, 0, 0]
    ends_processed = []

    for end in game.ends:
        end_info = [game.meta_data['tournament_id'],
                    game.meta_data['id'],
                    game.meta_data['round'],
                    game.teams[0].name,
                    game.teams[1].name,
                    end.number,
                    end.hammer,
                    end.hammer, 0]
        if end.score_0 > end.score_1:
            end_info[7] = 0
            end_info[8] = end.score_0
            cur_state[0] -= end.score_0
            cur_state[1] -= 1
            if end.hammer == 0:
                cur_state[2] -= end.score_0
                cur_state[3] -= 1
            else:
                cur_state[4] -= end.score_0
                cur_state[5] -= 1
        elif end.score_0 < end.score_1:
            end_info[7] = 1
            end_info[8] = end.score_1
            cur_state[0] += end.score_1
            cur_state[1] += 1
            if end.hammer == 1:
                cur_state[2] += end.score_1
                cur_state[3] += 1
            else:
                cur_state[4] += end.score_1
                cur_state[5] += 1
        else:  # blank
            cur_state[6] += 1
        end_info.extend(cur_state)
        end_info.append(game.meta_data['winner'])
        ends_processed.append(end_info)
    return ends_processed
