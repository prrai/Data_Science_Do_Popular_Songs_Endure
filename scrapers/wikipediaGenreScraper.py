import wikipedia
import bs4
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import re
import pandas as pd

path_final_csv = r'../data/'


def run_dates():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_release_genre_midtermdata'), encoding='latin-1')
    if 'Genres' not in base_df:
        base_df['Genres'] = ""
    scraped_pos = 4165
    scraped_pos_end = 4170
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
            # for current_page in pages:
            #     try:
            #         this_page = wikipedia.page(current_page)
            #     except:
            #         base_df.loc[i, 'Song_release_date'] = 0
            #         continue
            #     soup = BeautifulSoup(this_page.html(), "lxml")
            #     if len(str(soup).split('<th scope="row">Released</th>')) < 2:
            #         base_df.loc[i, 'Song_release_date'] = 0
            #         continue
            #     if len(str(soup).split('<th scope="row">Released</th>')[1].split('"plainlist">')) < 2:
            #         base_df.loc[i, 'Song_release_date'] = 0
            #         continue
            #     if len(str(soup).split('<th scope="row">Released</th>'
            #                                    )[1].split('"plainlist">')[1].split('<')) < 2:
            #         base_df.loc[i, 'Song_release_date'] = 0
            #         continue
            #     release_date = str(soup).split('<th scope="row">Released</th>'
            #                                    )[1].split('"plainlist">')[1].split('<')[0].strip()
            #     print(release_date)
            #     base_df.loc[i, 'Song_release_date'] = release_date
            #     break

            for current_page in pages:
                try:
                    this_page = wikipedia.page(current_page)
                except:
                    base_df.loc[i, 'Genres'] = ''
                    continue
                soup = BeautifulSoup(this_page.html(), "lxml")
                table = soup.find('table', {'class': "infobox vevent"})
                if not table:
                    base_df.loc[i, 'Genres'] = ''
                    continue
                genre_data = None
                for item in table.find_all('tr'):
                    if '/wiki/Music_genre' in str(item):
                        genre_data = str(item)
                        break
                if not genre_data:
                    base_df.loc[i, 'Genres'] = ''
                    continue
                genres = re.findall('/wiki/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                    genre_data)
                if len(genres) < 2:
                    base_df.loc[i, 'Genres'] = ''
                    continue
                genres = genres[1:]
                for j in range(0, len(genres)):
                    genres[j] = genres[j].split('/')[-1].lower()
                genres = ','.join(map(str, genres))
                print(genres)
                base_df.loc[i, 'Genres'] = genres
                break
            scraped_pos += 1
        base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_release_genre_midtermdata'), index=False)


if __name__ == '__main__':
    run_dates()