import bs4
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import pandas as pd
import re

data_path = r'../data/awards/oscars'
full_page = r'webpage.htm'
path_final_csv = r'../data/'


def run():
    html = open(os.path.join(data_path, full_page), 'r')
    soup = BeautifulSoup(html, "lxml")
    data = str(soup)
    data = re.findall('quot;([^"]*)&amp;quot;', data)
    with open(os.path.join(data_path, 'all_oscar_winners.txt'), 'w') as write_data:
        for i in range(0, len(data)):
            data[i] = data[i].replace('&amp;#39;', "'")
            write_data.writelines(data[i] + '\n')


def populate():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'after_movie_tv_feature_count'), encoding='latin-1')
    base_df['Oscars_won'] = ""

    with open(os.path.join(data_path, 'all_oscar_winners.txt'), 'r') as data:
        data = data.read().split('\n')
        data = data[:-1]
        for i, row in base_df.iterrows():
            if row.Title in data:
                base_df.loc[i, 'Oscars_won'] = 1
            else:
                base_df.loc[i, 'Oscars_won'] = 0
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'after_oscars'), index=False)

if __name__ == '__main__':
    run()
    populate()