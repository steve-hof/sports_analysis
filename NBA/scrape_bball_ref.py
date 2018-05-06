import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import re
import sys
import string
import requests
import datetime
# import progressbar2
import time

# page_request = requests.get(url)
# soup = BeautifulSoup(page_request.text)
# wrap = soup.find('div', {'id': 'wrap'})
# content = wrap.find('div', {'id': 'content'})
# all_per_poss = content.find('div', {'id': 'all_per_poss'})


def player_adv_stats(url):
    """
    scrape players page - navigate to advanced stats table

    :param url: url for particular player
    :return: data frame with players adv statistics

    """
    # Navigate to
    base_url = 'http://www.basketball-reference.com'
    full_url = base_url + url
    comm = re.compile("<!--|-->")
    page_request = requests.get(full_url, 'lxml')
    soup = BeautifulSoup(re.sub("<!--|-->", "", page_request.text))
    wrap = soup.find('div', {'id': 'wrap'})
    content = wrap.find('div', {'id': 'content'})
    all_adv = content.find('div', {'id': 'all_advanced'})
    table = all_adv.find('table', {'id': 'advanced'})
    t_foot = table.find('tfoot')
    t_r = t_foot.find('tr')

    pattern = r"\"([^{\"}]*)\""
    col_list = []
    stat_list = []
    for row in t_r.findAll('td'):
        stat_list.append(row.text)
        row = str(row)
        match = re.findall(pattern, row)
        col_list.append(match[1])
    col_list = col_list[4:]
    stat_list = stat_list[4:]
    cleaned_stat_list = []

    for i, st in enumerate(stat_list):
        try:
            st = float(st)
            cleaned_stat_list.append(st)
        except:
            print(f"fucking up at index {i}")
    player_entry = dict(zip(col_list, cleaned_stat_list))
    return player_entry


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

        fill = 12

    # create dictionary with all of the info
    player_entry = {'url': url,
                    'birth_place': birth_place,
                    'shoots': shoots,
                    'high_school': high_school,
                    'draft': draft,
                    'position_str': position_str}

    return player_entry


def player_info():
    '''
    This function web scrapes basketball-reference and extracts player's info.
    '''
    players = []
    base_url = 'http://www.basketball-reference.com/players/'

    # get player tables from alphabetical list pages
    # for letter in string.ascii_lowercase:
    for letter in 'q':
        page_request = requests.get(base_url + letter)
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
    save_path = 'scraped_data/players_general_info_' + letter + '.csv'
    df.to_csv(save_path, index=False)
    return df


def main():
    players_general_info = player_info()  # call function that scrapes general info

    player_adv_stats_list = []
    for i, url in enumerate(players_general_info.url):
        # try:
        player_adv_stats_list.append(player_adv_stats(url))
        # except:
        #     print(f"can't load: {url}; location {i}")
        time.sleep(0.1)
        fill = 12

    players_details_info_list = []
    for i, url in enumerate(players_general_info.url):
        try:
            players_details_info_list.append(player_detail_info(url))
        except:
            print('cannot load: %s; location %d' % (url, i))
        # bar.update(i)
        time.sleep(0.1)
    players_detail_df = pd.DataFrame(players_details_info_list)  # convert to dataframe
    players_df = players_general_info.merge(players_detail_df, how='outer', on='url')
    fill = 12



if __name__ == '__main__':
    main()
