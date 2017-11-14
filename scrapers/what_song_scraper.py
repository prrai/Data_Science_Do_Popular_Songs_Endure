import bs4
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import json
import requests
import pandas as pd

home_site = r'http://www.api.what-song.com/'
api = r'artist/songs/list/'
parameter_list = r'?artist='
data_path = r'../data/what_song/'

query_url = os.path.join(home_site, os.path.join(api, parameter_list))
total_artists = 28053


def run():
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    for i in range(282, total_artists + 1):
        print("########################################")
        page = "{}{}".format(query_url, i)
        print(page)
        response = requests.get(page)
        json_data = json.loads(response.text)
        if 'data' in json_data:
            file_name = json_data['data']['Artist']['slug']
            with open("{}/{}.txt".format(data_path, file_name), 'w') as write_data:
                for item in json_data['data']['SongList']:
                    write_data.writelines(item['title'] + '\n')
        print("########################################")

if __name__ == '__main__':
    run()
