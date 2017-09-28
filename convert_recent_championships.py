#!/usr/bin/env python3


import os
from pathlib import Path

import wcf

from processing.game import Game
from processing.pipeline import convert


def main():
    print(f'WCF API version {wcf.__version__}')
    print(os.getcwd())
    conn = wcf.API('../credentials/wcf.json').connect()

    men_wcc = [294, 290, 317, 355, 396, 405, 455, 488, 512, 555, 580]
    women_wcc = [255, 293, 313, 371, 402, 444, 454, 487, 507, 554, 579]
    years_wcc = list(range(2007, 2018))

    men_olympic = [273, 381]
    women_olympic = [274, 382]
    years_olympic = [2010, 2014]

    assert len(men_wcc) == len(women_wcc) == len(years_wcc)
    assert len(men_olympic) == len(women_olympic) == len(years_olympic)

    print('Processing men...')
    process_tourney_list(conn, men_wcc, years_wcc, 'men')
    process_tourney_list(conn, men_olympic, years_olympic, 'men')
    print('Processing women...')
    process_tourney_list(conn, women_wcc, years_wcc, 'women')
    process_tourney_list(conn, women_olympic, years_olympic, 'women')
    print('Done')


def process_tourney_list(conn, tourney_ids, years, type_):
    assert type_ in ('men', 'women')
    out_directory = Path('data') / type_
    for id_, year in zip(tourney_ids, years):
        filename = out_directory / f'{id_:03d}.csv'
        if not filename.exists():
            print(f'  {id_}, {year}')
            process_single_tourney(conn, id_, year, filename)


def process_single_tourney(conn, id_, year, filename):
    tourney = conn.get_draws_by_tournament(id_)
    games = [Game(g).convert() for g in tourney]
    df = convert(games)
    df['year'] = year
    df.to_csv(str(filename), index=False)


if __name__ == '__main__':
    main()
