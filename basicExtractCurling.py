#!/usr/bin/env python3


import argparse
import csv
import re
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', type=str)
    parser.add_argument('-o', '--outfile', type=str)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    print(args)
    data = get_data_from(args.infile)
    game_data = save_box_scores(data)
    print(game_data)


def get_data_from(filename):
    with open(filename, 'rU') as f:
        data = [line.strip() for line in f if line.strip() != '']
    draw_start = 'SCORING AND PERCENTAGES SUMMARY FOR DRAW 1'
    index = data.index(draw_start)
    return data[index:]


def save_box_scores(data):
    box_scores = []
    game = []
    box_match = re.compile('\d +\d +\d +\d')
    for line in data:
        matches = re.findall(box_match, line)
        if matches:
            game.append(line.strip())
        if len(game) == 3:
            box_scores.append(game[1:])
            game = []
    return box_scores


if __name__ == "__main__":
    main()
