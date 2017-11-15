import bs4
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import pandas as pd

data_path = r'../data/what_song/'
path_final_csv = r'../data/'


def run():
    data_frame = pd.DataFrame(columns=['Song', 'Artist'])
    name_list = []
    for path, sub_dirs, name_list in os.walk(data_path):
        pass
    for file_name in name_list:
        try:
            print("Processing: {}".format(file_name))
            with open(data_path + file_name, 'r') as data:
                data = data.read().split('\n')
                for item in data:
                    if len(item):
                        data_frame = data_frame.append([{
                            'Song': item, 'Artist': file_name.split('.txt')[0]}])
        except IOError:
            print("Failed for: {}".format(file_name))
    data_frame.to_csv('{0}/{1}.csv'.format(data_path, 'all_songs_and_artists'), index=False)


def group():
    df = pd.read_csv('{0}/{1}.csv'.format(data_path, 'all_songs_and_artists'))
    df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0: 'count'})
    df.to_csv('{0}/{1}.csv'.format(data_path, 'group_songs_and_artists'), index=False)


def match():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'with_popularity2'), encoding='latin-1')
    base_df['Movies_TV_feature_count'] = ""
    df = pd.read_csv('{0}/{1}.csv'.format(data_path, 'group_songs_and_artists'), encoding='latin-1')
    for i, row in base_df.iterrows():
        matched_df = df.loc[df['Song'] == row.Title]
        curr_count = 0
        if len(matched_df):
            row_artist_tokens = row.Artist.lower().split()
            for row2 in matched_df.itertuples():
                slugged_tokens = row2.Artist.lower().split('-')
                token_matches = 0
                for token in row_artist_tokens:
                    for slug in slugged_tokens:
                        if token == slug and token not in ['and', 'the', 'with', 'feat']:
                            token_matches += 1
                    if token_matches > 1:
                        break
                if token_matches > 1:
                    print("Matched {} with {}".format(row.Artist, row2.Artist))
                    curr_count += row2.count
        base_df.loc[i, 'Movies_TV_feature_count'] = int(curr_count)
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'after_movie_tv_feature_count'), index=False)

if __name__ == '__main__':
    # run()
    # group()
    match()
