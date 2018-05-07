#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import json


def acquire_gameData(data):
    import requests
    header_data = {  # I pulled this header from the py goldsberry library
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9' \
                  ',image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }
    game_url = 'http://stats.nba.com/stats/playbyplayv2?EndPeriod=0&EndRange=0&GameID=' + data['gameid'] + \
               '&RangeType=0&StartPeriod=0&StartRange=0'  # address for querying the data
    response = requests.get(game_url, headers=header_data)  # go get the data
    headers = response.json()['resultSets'][0]['headers']  # get headers of data
    gameData = response.json()['resultSets'][0]['rowSet']  # get actual data from json object
    df = pd.DataFrame(gameData, columns=headers)  # turn the data into a pandas dataframe
    df = df[[df.columns[1], df.columns[2], df.columns[7], df.columns[9],
             df.columns[18]]]  # there's a ton of data here, so I trim  it doown
    df['TEAM'] = df['PLAYER1_TEAM_ABBREVIATION']
    df = df.drop('PLAYER1_TEAM_ABBREVIATION', 1)
    return df


json_data = open('/Users/stevehof/school/comp/fun/Winning_in_Sports_with_Data/NBA/scraped_data/sports_vu_2016.json')
data = json.load(json_data)
keys_d = data.keys()
h = data['events'][0].keys()
m = data['events'][0]['moments'][0]

df = acquire_gameData(data)
show = df.head()
fill = 12
