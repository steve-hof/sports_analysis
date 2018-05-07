#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
import json


# Animation function / loop
def draw_court(axis):
    import matplotlib.image as mpimg
    img = mpimg.imread('./nba_court_T.png')  # read image. I got this image from gmf05's github.
    plt.imshow(img, extent=axis, zorder=0)  # show the image.


def animate(
        n):  # matplotlib's animation function loops through a function n times that draws a different frame on each iteration
    for i, ii in enumerate(player_xy[n]):  # loop through all the players
        player_circ[i].center = (ii[1], ii[2])  # change each players xy position
        player_text[i].set_text(str(jerseydict[ii[0]]))  # draw the text for each player.
        player_text[i].set_x(ii[1])  # set the text x position
        player_text[i].set_y(ii[2])  # set text y position
    ball_circ.center = (ball_xy[n, 0], ball_xy[n, 1])  # change ball xy position
    ball_circ.radius = 1.1  # i could change the size of the ball according to its height, but chose to keep this constant
    return tuple(player_text) + tuple(player_circ) + (ball_circ,)


def init():  # this is what matplotlib's animation will create before drawing the first frame.
    for i in range(10):  # set up players
        player_text[i].set_text('')
        ax.add_patch(player_circ[i])
    ax.add_patch(ball_circ)  # create ball
    ax.axis('off')  # turn off axis
    dx = 5
    plt.xlim([0 - dx, 100 + dx])  # set axis
    plt.ylim([0 - dx, 50 + dx])
    return tuple(player_text) + tuple(player_circ) + (ball_circ,)


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
             df.columns[18]]]  # there's a ton of data here, so I trim  it down
    df['TEAM'] = df['PLAYER1_TEAM_ABBREVIATION']
    df = df.drop('PLAYER1_TEAM_ABBREVIATION', 1)
    return df


def find_moment(search_id):
    for i, events in enumerate(data['events']):
        if events['eventId'] == str(search_id):
            finder = i
            break
    return finder


json_data = open('/Users/stevehof/school/comp/fun/Winning_in_Sports_with_Data/'
                 'NBA/scraped_data/sports_vu_2016.json')
data = json.load(json_data)
keys_d = data.keys()
h = data['events'][0].keys()
m = data['events'][0]['moments'][0]

df = acquire_gameData(data)
show = df.head()

player_fields = data['events'][0]['home']['players'][0].keys()
home_players = pd.DataFrame(data=[i for i in data['events'][0]['home']['players']], columns=player_fields)
away_players = pd.DataFrame(data=[i for i in data['events'][0]['visitor']['players']], columns=player_fields)
players = pd.merge(home_players, away_players, how='outer')
jerseydict = dict(zip(players.playerid.values, players.jersey.values))

# the order of events does not match up, so we have to use the eventIds.
# This loop finds the correct event for a given id#.
search_id = 41

event_num = find_moment(search_id)
ball_xy = np.array([x[5][0][2:5] for x in data['events'][event_num]['moments']])  # create matrix of ball data
player_xy = np.array(
    [np.array(x[5][1:])[:, 1:4] for x in data['events'][event_num]['moments']])  # create matrix of player data
fill = 12
