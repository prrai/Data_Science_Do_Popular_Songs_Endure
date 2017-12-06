import wikipedia
import bs4
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import re
import requests
import pandas as pd

path_final_csv = r'../data/'


def run_dates():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_release_genre_midtermdata'), encoding='latin-1')
    if 'Genres' not in base_df:
        base_df['Genres'] = ""
    scraped_pos_start = 0
    scraped_pos_end = 5000
    scraped_pos = scraped_pos_start
    for i, rows in base_df.iterrows():
        if i < scraped_pos:
            continue
        if i > scraped_pos_end:
            exit(0)
        current_song = rows.Title
        current_artist = rows.Artist
        print("i = {} : Lookup: Song: {}, Artist: {}".format(i, current_song, current_artist))
        query = '{} {}'.format(current_song, current_artist)
        query = query.replace(" ", "+")
        r = requests.get(
            'https://www.google.com/search?q={}&gbv=1&sei=YwHNVpHLOYiWmQHk3K24Ct'.format(query))
        soup = BeautifulSoup(r.text, "lxml")
        genre = str(soup).split('Genre: </span><span class=')
        if len(genre) > 1:
            val = genre[1].split('<')[0].split('>')[1]
        else:
            genre = str(soup).split('Genres: </span><span class=')
            if len(genre) > 1:
                val = genre[1].split('<')[0].split('>')[1]
            else:
                val = ''
        print(val)
        base_df.loc[i, 'Genres'] = val
        scraped_pos += 1
        base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_release_genre_midtermdata_{}_{}'.format(
            scraped_pos_start, scraped_pos_end)), index=False)


if __name__ == '__main__':
    run_dates()