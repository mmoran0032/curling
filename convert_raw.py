#!/usr/bin/env python3


import json


data_directory = 'data/raw'
output_directory = 'data/processed'

filename = '{}/555.json'.format(data_directory)
with open(filename, 'r') as f:
    data = json.load(f)

for game in data:
    print(game['Team1']['Team']['Code'],
          game['Team2']['Team']['Code'])
