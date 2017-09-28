#!/usr/bin/env python3


from enum import Enum


class Result(Enum):
    WIN = 2
    DRAW = 1
    LOSS = 0


def get_new_rating(rating, opponent, result, k_factor=30):
    expected = _get_expected_score(rating, opponent)
    return _calculate_new(rating, result, expected, k_factor)


def _get_expected_score(rating, opponent):
    return 1 / (1 + 10**((opponent - rating) / 400))


def _calculate_new(rating, score, expected, k_factor):
    return int(rating + k_factor * (score.value / 2 - expected))


if __name__ == '__main__':
    assert get_new_rating(1500, 1500, Result.WIN) == 1515
    assert get_new_rating(1500, 1500, Result.DRAW) == 1500
    assert get_new_rating(1500, 1500, Result.LOSS) == 1485
    print('all tests passed')
