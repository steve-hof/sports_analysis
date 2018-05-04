#!/usr/bin/env python3

import NBAapi as nba
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from scipy import misc
from scipy.stats.stats import pearsonr


def main():
    years = '2014-15'
    shotchart, leagueavergae = nba.shotchart.shotchartdetail(season=years)  # get shot chart data from NBA.stats
    shotchart['PLAYER'] = list(zip(shotchart['PLAYER_NAME'], shotchart['PLAYER_ID']))
    print(shotchart.head())
    zones_list = [(u'Less Than 8 ft.', u'Center(C)'),
                  (u'8-16 ft.', u'Center(C)'),
                  (u'8-16 ft.', u'Left Side(L)'),
                  (u'8-16 ft.', u'Right Side(R)'),
                  (u'16-24 ft.', u'Center(C)'),
                  (u'16-24 ft.', u'Left Side Center(LC)'),
                  (u'16-24 ft.', u'Left Side(L)'),
                  (u'16-24 ft.', u'Right Side Center(RC)'),
                  (u'16-24 ft.', u'Right Side(R)'),
                  (u'24+ ft.', u'Center(C)'),
                  (u'24+ ft.', u'Left Side Center(LC)'),
                  (u'24+ ft.', u'Left Side(L)'),
                  (u'24+ ft.', u'Right Side Center(RC)'),
                  (u'24+ ft.', u'Right Side(R)'),
                  (u'Back Court Shot', u'Back Court(BC)')]

    # Create dataframe with PLAYER as index and the rest as columns
    zones = shotchart.groupby(['SHOT_ZONE_RANGE', 'SHOT_ZONE_AREA', 'SHOT_MADE_FLAG',
                               'PLAYER']).size().unstack(fill_value=0).T

    players = nba.player.biostats(season='2016-17')
    players['PLAYER'] = list(zip(players['PLAYER_NAME'], players['PLAYER_ID']))
    players.set_index('PLAYER', inplace=True)

    GP = players.loc[:, ['GP']]  # create DataFrame with single GP column
    GP.columns = pd.MultiIndex.from_product(
        [GP.columns, [''], ['']])  # change column to multiindex before join (prevents join warning)
    zones_with_GP = zones.join(GP)  # only included game played from players
    zones_with_GP.columns = pd.MultiIndex.from_tuples(zones_with_GP.columns.tolist(),
                                                      names=['SHOT_ZONE_RANGE', 'SHOT_ZONE_AREA', 'MADE'])
    # zones_with_GP = zones_with_GP.sortlevel(0, axis=1)  # sort columns for better performance (+ avoid warning)

    path = os.path.dirname(nba.__file__)  # get path of the nba module
    # floor = misc.imread(path + '\\data\\court.jpg')  # load floor template
    plt.figure(figsize=(15, 12.5), facecolor='white')  # set up figure
    ax = nba.plot.court(lw=4, outer_lines=False)  # plot NBA court - don't include the outer lines
    ax.axis('off')
    nba.plot.zones(lw=2, color='white', linewidth=3)
    eligible = zones_with_GP.loc[:, 'GP'].values > 10  # only include players which player more than 10 games
    # we are going to use the zone_list to plot information in each zone
    for zone in zones_list:
        # calculate shots per game for specific zone and sort from highest to lowest
        shots_PG = (zones_with_GP.loc[eligible, zone].sum(axis=1) / zones_with_GP.loc[eligible, 'GP']).sort_values(0,
                                                                                                                   ascending=False)
        name = []  # will be used to store the text we want to print
        # run a loop to find top 3 players
        for j in range(3):
            # create text
            name.append(shots_PG.index[j][0].split(' ')[0][0] + '. ' + shots_PG.index[j][0].split(' ')[1] + ':%0.1f' %
                        shots_PG.values[j])
        nba.plot.text_in_zone('\n'.join(name), zone, color='black', backgroundcolor='white', alpha=1)
    title = 'Most Shots by Zone, ' + years
    plt.title(title, fontsize=16)
    # plt.imshow(floor, extent=[-30, 30, -7, 43])  # plot floor

    plt.show()

    # Plot FG%
    plt.figure(figsize=(15, 12.5), facecolor='white')
    ax = nba.plot.court(lw=4, outer_lines=False)
    ax.axis('off')
    nba.plot.zones(color='gray')
    eligible = zones_with_GP.loc[:, 'GP'].values > 10
    for zone in zones_list:
        # create new dataframe with total shot, shots per game and FG%
        df = pd.concat([zones_with_GP.loc[eligible, zone].sum(axis=1),
                        zones_with_GP.loc[eligible, zone].sum(axis=1) / zones_with_GP.loc[eligible, 'GP'],
                        100.0 * zones_with_GP.loc[eligible, (zone[0], zone[1], 1)] / zones_with_GP.loc[
                            eligible, zone].sum(axis=1)], axis=1)
        df.columns = ['SHOTS', 'SHOTS_PG', 'FGP']

        # only include players that have a total of more than 10 shots or are in the top 100 in shots taken (from that zone)
        top100 = df.loc[:, 'SHOTS_PG'].sort_values(0, ascending=False)[100]
        if zone != (u'Back Court Shot', u'Back Court(BC)'):
            mask = (df.loc[:, 'SHOTS_PG'] >= top100) & (df.loc[:, 'SHOTS'] >= 10)
        else:
            mask = (df.loc[:, 'SHOTS'] >= 2)
            # sort by FG%
        perc_leaders = df.iloc[mask.values, :].sort_values('FGP', ascending=False)
        name = []
        for j in range(3):
            name.append(perc_leaders.index[j][0].split(' ')[0][0] + '. ' + perc_leaders.index[j][0].split(' ')[
                1] + ': %0.1f (%d)' % (perc_leaders.ix[j, 'FGP'], perc_leaders.ix[j, 'SHOTS']))
        nba.plot.text_in_zone('\n'.join(name), zone, color='black', backgroundcolor='white', alpha=1)
    title = 'Highest Field Goal % by Zone, ' + years
    plt.title(title, fontsize=16)
    plt.text(-15, -7, 'Player: FG % \n (total shots)', horizontalalignment='center')

    plt.show()
    fill = 12


if __name__ == '__main__':
    main()
