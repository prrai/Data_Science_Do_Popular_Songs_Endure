import bs4
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import pandas as pd
import re

data_path = r'../data/awards/grammy'
home_site = r'http://www.grammy.com/'
path_final_csv = r'../data/'


def run():
    home_page = r'grammys/awards/lifetime-awards'
    page = home_site + home_page
    conn = urlopen(page)
    html = conn.read()
    soup = BeautifulSoup(html, "lxml")
    table_header = soup.find('table', {'class': 'bodytext'}).find_all('strong')
    with open(os.path.join(data_path, 'lifetime_achievement_artists.txt'), 'w') as write_data:
        for item in table_header:
            write_data.writelines(item.string.strip() + '\n')


def populate():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'after_oscars'), encoding='latin-1')
    base_df['Artist_lifetime_grammy_achievement'] = ""

    with open(os.path.join(data_path, 'lifetime_achievement_artists.txt'), 'r') as data:
        data = data.read().split('\n')
        data = data[:-1]
        for i, row in base_df.iterrows():
            row_artist_tokens = row.Artist.lower().split()
            matched = False
            for item in data:
                data_tokens = item.lower().split()
                token_matches = 0
                for token in row_artist_tokens:
                    for slug in data_tokens:
                        if token == slug and token not in ['and', 'the', 'with', 'feat']:
                            token_matches += 1
                    if token_matches > 1:
                        break
                if token_matches > 1:
                    print("Matched {} with {}".format(row.Artist, item))
                    base_df.loc[i, 'Artist_lifetime_grammy_achievement'] = 1
                    matched = True
                    break
            if not matched:
                base_df.loc[i, 'Artist_lifetime_grammy_achievement'] = 0
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'after_grammy_lifetime_achievement'), index=False)


def wins_and_nominations():
    home_page = r'grammys/artists/'
    page = home_site + home_page
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'after_grammy_lifetime_achievement'), encoding='latin-1')
    base_df['Artist_grammy_nominations'] = ""
    base_df['Artist_grammy_wins'] = ""
    ctr = 1
    for i, row in base_df.iterrows():
        row_artist_tokens = row.Artist.lower().split()
        print(i)
        for j in range(1, len(row_artist_tokens) + 1):
            slugged = '-'.join(row_artist_tokens[0:j])
            try:
                conn = urlopen(page + slugged)
                html = conn.read()
                soup = BeautifulSoup(html, "lxml")
                table = soup.find_all('div', {'class': 'field-item even'})
                base_df.loc[i, 'Artist_grammy_nominations'] = int(table[0].string)
                base_df.loc[i, 'Artist_grammy_wins'] = int(table[1].string)
                # print("Worked fine for: {}, wins={}, nominations={}, ctr= {}".format(slugged, int(table[1].string),
                                                                                     # int(table[0].string), ctr))
                ctr += 1
                break
            except:
                # print("Failed for: {}".format(slugged))
                base_df.loc[i, 'Artist_grammy_nominations'] = 0
                base_df.loc[i, 'Artist_grammy_wins'] = 0

    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'after_grammy_nominations_wins'), index=False)


if __name__ == '__main__':
    # run()
    # populate()
    wins_and_nominations()
