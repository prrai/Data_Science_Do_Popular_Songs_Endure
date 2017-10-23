import bs4
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import pandas as pd

home_site = r'http://www.umdmusic.com/'
home_page = r'default.asp?Lang=English&Chart=D&ChDay=1&ChMonth=1&ChYear=1959&ChBand=&ChSong='
last_week = r'October_28_2017'
data_path = r'../data/umd/'


def get_week(soup):
    table_header = soup.find('table', {'style': 'font-size:10pt;font-family:Arial'})
    week = '_'.join(table_header.find('td', {'align': 'right'}).find('b').
                         string.strip('\r\n').split()).replace(',', '')
    return week


def get_data_for_page(soup):
    data_frame = pd.DataFrame(columns=['Title', 'Artist', 'Entry_Date', 'Entry_Position', 'Peak_Position',
                                       'Total_Weeks'])
    chart_table = soup.find_all('table', {'border': 1})[-1]
    rows = chart_table.find_all('tr')
    rows = rows[2:]

    for item in rows:
        title_artist = item.find('td', {'style': 'font-size:10pt;font-family:Arial;padding-left:0.1in'})
        title_artist_str = str(title_artist)
        title = title_artist.find('b').string.strip()
        artist = title_artist_str.split('<br/>')[1].split('</td>')[0].strip()
        stats = item.find_all('td', {'style': 'font-size:10pt;font-family:Arial'})
        entry_date = stats[4].string.strip()
        entry_position = int(stats[5].string)
        peak_position = int(stats[6].string)
        total_weeks = int(stats[7].string)
        data_frame = data_frame.append([{
            'Title': title, 'Artist': artist, 'Entry_Date': entry_date, 'Entry_Position': entry_position,
            'Peak_Position': peak_position, 'Total_Weeks': total_weeks}])
    return data_frame


def run():
    page = home_site + home_page
    curr_week = None
    while curr_week != last_week:
        print(page)
        conn = urlopen(page)
        html = conn.read()
        soup = BeautifulSoup(html, "lxml")
        curr_week = get_week(soup)
        curr_dir = os.path.join(data_path, curr_week)
        if not os.path.exists(curr_dir):
            os.makedirs(curr_dir)
        print("***********************************************")
        print("Scraping for the week: {}".format(curr_week))
        print("***********************************************")
        data_frame = get_data_for_page(soup)
        data_frame.to_csv('{0}/{1}.csv'.format(curr_dir, curr_week), index=False)
        next_link_div = soup.find_all('table', {'border': 0, 'width': "100%"})[-1]
        page = next_link_div.find('td', {'align': 'right'}).find('a')['href']
        page = home_site + page

if __name__ == '__main__':
    run()
