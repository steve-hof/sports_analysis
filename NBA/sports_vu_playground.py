#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib as mpl
import json
import requests


# need the play by play data so we know what sports_vu data we're looking at
# this function

def get_pbp_game_data(data):
    header_data = {  # got the header from the py goldsberry library
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
               '&RangeType=0&StartPeriod=0&StartRange=0'
    page_request = requests.get(game_url, headers=header_data)
    # get the header data and add it to json
    headers = page_request.json()['resultSets'][0]['headers']

    # get the actual data 'rowSet' is the key we need
    pbp_game_data = page_request.json()['resultSets'][0]['rowSet']

    # create data frame
    df = pd.DataFrame(pbp_game_data, columns=headers)

    # only want certain columns
    cols = ['EVENTNUM', 'EVENTMSGTYPE', 'HOMEDESCRIPTION', 'VISITORDESCRIPTION',
            'PLAYER1_TEAM_ABBREVIATION']
    df = df[cols]

    # names of columns are horrid
    df['TEAM'] = df['PLAYER1_TEAM_ABBREVIATION']
    df.drop('PLAYER1_TEAM_ABBREVIATION', inplace=True, axis=1)

    # make dictionary so I don't have to memorize event type codes
    event_dict = {1: 'Make', 2: 'Miss', 3: 'Free Throw', 4: 'Rebound',
                  5: 'OB or T/O or Steal', 6: 'Personal Foul', 7: 'Violation',
                  8: 'Substitution', 9: 'Timeout', 10: 'Jump Ball',
                  12: '?-start quarter 1', 13: '?- start quarter2'}
    df['EVENTDESCR'] = df['EVENTMSGTYPE'].map(event_dict)
    cols = ['EVENTNUM', 'EVENTMSGTYPE', 'EVENTDESCR', 'HOMEDESCRIPTION',
            'VISITORDESCRIPTION', 'TEAM']
    df = df[cols]
    return df


def draw_court(axis):
    import matplotlib.image as mpimg
    img = mpimg.imread('scraped_data/nba_court_T.png')  # ot this image from gmf05's github.
    plt.imshow(img, extent=axis, zorder=0)  # show the image.


# This builds the base of the plot that the animation will take place on top of
def init_plot():
    # ten players on the court
    for i in range(10):
        pass


def find_moment(data, id):
    for i, events in enumerate(data['events']):
        if events['eventId'] == str(id):
            moment = i
            break
    return moment


def animate(player_xy, n):
    pass


def main():
    json_data = open('/Users/stevehof/school/comp/fun/Winning_in_Sports_with_Data/'
                     'NBA/scraped_data/sports_vu_2016.json')
    """

    Json_data is a dict w/ 3 keys: ['gamedate', gameid', 'events']
    
    Each event has 4 keys: ['eventId', 'visitor', 'home', 'moments']

    The numbers, for a moment, in order, are:
    1) quarter number.
    2) time of the event in milliseconds.
    3) number of seconds left in the quarter
    4) number of seconds left on the shot clock.
    No clue what 'none' represents, haha
    
    Then there is another matrix (11x5) where each row is:
    [0] Location of the ball
    [1:5] Locations of each of 5 home team players
    [6:11] Locations of each of 5 visitor team players
    
    The columns are:
    [0] Team ID (-1 for ball)
    [1] Player ID (-1 for ball)
    [2] x coordinate
    [3] y coordinate
    [4] z coordinate
    
    """

    data = json.load(json_data)
    first_event = data['events'][0].keys()
    first_moment = data['events'][0]['moments'][0]
    play_by_play_df = get_pbp_game_data(data)

    # Create players data frame for access to jersey number during animation
    blah = data['events'][0]['home']['players']
    player_cols = data['events'][0]['home']['players'][0].keys()
    home_players_df = pd.DataFrame(data=[i for i in data['events'][0]['home']['players']],
                                   columns=player_cols)
    visitor_players_df = pd.DataFrame(data=[i for i in data['events'][0]['visitor']['players']],
                                      columns=player_cols)
    players_df = pd.merge(home_players_df, visitor_players_df, how='outer')
    jersey_dict = dict(zip(players_df.playerid.values, players_df.jersey.values))

    # Find proper event number
    event_num = find_moment(data, 41)

    # Create matrices for ball and player positions
    ball_coords = np.array([x[5][0][2:5] for x in data['events'][event_num]['moments']])
    player_coords = np.array([np.array(x[5][1:])[:, 1:4] for x in data['events'][event_num]['moments']])
    print(ball_coords[0:10])
    # Draw the court
    fig = plt.figure(figsize=(15, 7.5))
    ax = plt.gca()
    draw_court([0, 100, 0, 50])
    plt.show()

    fill = 2


if __name__ == '__main__':
    main()
