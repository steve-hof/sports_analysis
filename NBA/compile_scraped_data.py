#!/usr/bin/env python3

import numpy as np
import pandas as pd
from career_scraper import get_100, get_100_cols, get_shooting, \
    get_shoot_cols, get_advanced, get_adv_cols
import requests
from bs4 import BeautifulSoup, SoupStrainer
import time

save_path = 'scraped_data/players_general_info.csv'


def player_general_info():
    '''
    This function web scrapes basketball-reference and extracts player's info.
    '''
    players = []
    players_base_url = 'http://www.basketball-reference.com/players/'

    # get player tables from alphabetical list pages
    # for letter in string.ascii_lowercase:
    for letter in 'q':
        page_request = requests.get(players_base_url + letter)
        soup = BeautifulSoup(page_request.text, "lxml")
        # find table in soup
        table = soup.find('table')

        if table:
            table_body = table.find('tbody')

            # loop over list of players
            for row in table_body.findAll('tr'):
                # get name and url
                player_url = row.find('a')
                player_names = player_url.text
                player_pages = player_url['href']

                # get some player's info from table
                cells = row.findAll('td')
                active_from = int(cells[0].text)
                active_to = int(cells[1].text)
                position = cells[2].text
                height = cells[3].text
                weight = cells[4].text
                birth_date = cells[5].text
                college = cells[6].text

                # create entry
                player_entry = {'url': player_pages,
                                'name': player_names,
                                'active_from': active_from,
                                'active_to': active_to,
                                'position': position,
                                'college': college,
                                'height': height,
                                'weight': weight,
                                'birth_date': birth_date}

                # append player dictionary
                players.append(player_entry)

    df = pd.DataFrame(players)

    return df


def player_detail_info(url):
    '''
    scrape player's personal page. Input is players url (without  www.basketball-reference.com)
    '''
    # we do not need to parse the whole page since the information we are interested in is only a small part
    personal = SoupStrainer('p')
    page_request = requests.get('http://www.basketball-reference.com' + url)
    soup = BeautifulSoup(page_request.text, "lxml", parse_only=personal)  # parse only part we are interested in
    p = soup.findAll('p')

    # initialize some values - sometimes they are not available
    shoots = None
    birth_place = None
    high_school = None
    draft = None
    position_str = None

    # loop over personal info to get certain information
    for prow in p:
        # look for shoots field
        if 'Shoots:' in prow.text:
            s = prow.text.replace('\n', '').split(u'\u25aa')  # clean text
            if len(s) > 1:
                shoots = s[1].split(':')[1].lstrip().rstrip()
        # look for position
        elif 'Position:' in prow.text:
            s = prow.text.replace('\n', '').split(u'\u25aa')
            if len(s) > 1:
                position_str = s[0].split(':')[1].lstrip().rstrip()
            else:
                position_str = prow.text.split('Position:')[
                    1].lstrip().rstrip()  # when shoots does not exist we need this
        # look for born
        elif 'Born:' in prow.text:
            s = prow.text.split(u'in\xa0')  # clean text
            if len(s) > 1:
                birth_place = s[1]
        elif 'High School:' in prow.text:
            s = prow.text.replace('\n', '').split(':')
            if len(s) > 1:
                high_school = s[1].lstrip()
        elif 'Draft:' in prow.text:
            s = prow.text.replace('\n', '').split(':')
            if len(s) > 1:
                draft = s[1].lstrip()

    # create dictionary with all of the info
    player_entry = {'url': url,
                    'birth_place': birth_place,
                    'shoots': shoots,
                    'high_school': high_school,
                    'draft': draft,
                    'position_str': position_str}

    return player_entry


def main():
    # player_info = player_general_info()  # call function that scrapes general info
    #
    # players_details_info_list = []
    # for i, url in enumerate(player_info.url):
    #     try:
    #         players_details_info_list.append(player_detail_info(url))
    #     except:
    #         print('cannot load: %s; location %d' % (url, i))
    #     # bar.update(i)
    #     time.sleep(0.1)
    # players_detail_df = pd.DataFrame(players_details_info_list)  # convert to dataframe
    # players_df = player_info.merge(players_detail_df, how='outer', on='url')
    #
    # players_df.to_csv(save_path, index=False)

    """
    Below is the code that generates the more detailed statistical 
    information and stores is in ________
    
    """
    player_info_df = pd.read_csv(save_path)

    temp_list = []

    # Web scrape data
    for url in player_info_df.url:
        url = 'http://www.basketball-reference.com' + url
        # Select which tables to scrape from
        per_100 = get_100(url)
        shooting = get_shooting(url)
        advanced = get_advanced(url)

        # Build dataframe in order
        df = [per_100, shooting, advanced]
        player_stats = []
        for sublist in df:
            for val in sublist:
                player_stats.append(val)

        # Save to temporary list
        temp_list.append(player_stats)

    # Get columns
    per_100_cols = get_100_cols()
    shoot_cols = get_shoot_cols()
    advanced_cols = get_adv_cols()

    tmp_list1 = [per_100_cols, shoot_cols, advanced_cols]
    cols = []
    for sublist in tmp_list1:
        for val in sublist:
            cols.append(val)

    # Make data frame
    new_stats_df = pd.DataFrame(temp_list, columns=cols)
    full_player_stats_df = pd.merge(player_stats, new_stats_df, on='Player_ID', how='right')

    fill = 12


if __name__ == '__main__':
    main()
