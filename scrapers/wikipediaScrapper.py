import wikipedia
import bs4
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import re
import pandas as pd

path_final_csv = r'../data/final'


def run_dates():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_date_final'), encoding='latin-1')
    if 'Song_release_date' not in base_df:
        base_df['Song_release_date'] = ""
    if 'Genres' not in base_df:
        base_df['Genres'] = ""
    scraped_pos_start = 20001
    scraped_pos_end = 21000
    scraped_pos = scraped_pos_start
    for i, rows in base_df.iterrows():
        if i < scraped_pos:
            continue
        if i > scraped_pos_end:
            exit(0)
        current_song = rows.Title
        current_artist = rows.Artist
        print("i = {} : Lookup: Song: {}, Artist: {}".format(i, current_song, current_artist))
        pages = wikipedia.search('{} {}'.format(current_song, current_artist))
        if pages:
            for current_page in pages:
                try:
                    this_page = wikipedia.page(current_page)
                except:
                    base_df.loc[i, 'Song_release_date'] = 0
                    continue
                soup = BeautifulSoup(this_page.html(), "lxml")
                if len(str(soup).split('<th scope="row">Released</th>')) < 2:
                    base_df.loc[i, 'Song_release_date'] = 0
                    continue
                if len(str(soup).split('<th scope="row">Released</th>')[1].split('"plainlist">')) < 2:
                    base_df.loc[i, 'Song_release_date'] = 0
                    continue
                if len(str(soup).split('<th scope="row">Released</th>'
                                               )[1].split('"plainlist">')[1].split('<')) < 2:
                    base_df.loc[i, 'Song_release_date'] = 0
                    continue
                release_date = str(soup).split('<th scope="row">Released</th>'
                                               )[1].split('"plainlist">')[1].split('<')[0].strip()
                print(release_date)
                base_df.loc[i, 'Song_release_date'] = release_date
                break
            scraped_pos += 1
        base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_date_final2_{}_{}'.format(
            scraped_pos_start, scraped_pos_end)), index=False)


if __name__ == '__main__':
    run_dates()