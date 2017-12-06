import os
import numpy as np
import pandas as pd

path_final_csv = r'../data/final'


def run():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'midtermdata'), encoding='latin-1')
    base_df = base_df[base_df.Popularity != -1]
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'clean_midtermdata'), index=False)


def update_date():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'clean_midtermdata'), encoding='latin-1', parse_dates=True)
    base_df['Entry_Year'] = None
    for i, rows in base_df.iterrows():
        base_df.loc[i, 'Entry_Year'] = int(base_df['Entry_Date'][i].split('/')[2])
        if base_df.loc[i, 'Entry_Year'] > 17:
            base_df.loc[i, 'Entry_Year'] += 1900
        else:
            base_df.loc[i, 'Entry_Year'] += 2000
    base_df = base_df[base_df.Entry_Year < 2014]
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_date_midtermdata'), index=False)


def merge_start_date():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_date_midtermdata'), encoding='latin-1')
    df2 = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_date_final'), encoding='latin-1')
    results = dict()
    df2['Song_release_date'] = ""
    for i, rows in base_df.iterrows():
        results[rows.Title] = rows.Song_release_date

    for i, rows in df2.iterrows():
        if rows.Title not in results:
            print("Didn't find: {}".format(rows.Title))
        else:
            df2.loc[i, 'Song_release_date'] = results[rows.Title]

    df2.to_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_date_final2'), index=False)


def process_age_distribution():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'age_distribution'), encoding='latin-1')
    df2 = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'final_unnormalized_dataset'), encoding='latin-1')
    results = dict()
    for i, rows in base_df.iterrows():
        results[rows.Year] = rows.Percentage

    df2['Age_Percentage_15_30'] = ""
    for i, rows in df2.iterrows():
        df2.loc[i, 'Age_Percentage_15_30'] = results[rows.Entry_Year]
    df2.to_csv('{0}/{1}.csv'.format(path_final_csv, 'final_unnormalized_dataset'), index=False)


def normalized_data():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'final_unnormalized_dataset'), encoding='latin-1')
    for column in base_df:
        if column == 'Title' or column == 'Artist' or column == 'Entry_Date' or column == 'release_date':
            continue
        if column == 'Youtube viewcount':
            base_df[column] /= 2
        base_df[column].fillna((base_df[column].median()), inplace=True)
        if column == 'Youtube viewcount':
            base_df[column] = np.log10(base_df[column])
            base_df[column].replace(to_replace=[np.inf, -np.inf, np.NaN], value=0, inplace=True)
        elif column == 'Popularity':
            base_df[column] = 5 * np.log10(base_df[column])
            base_df[column].replace(to_replace=[np.inf, -np.inf, np.NaN], value=0, inplace=True)
            # base_df[column] = (base_df[column] - base_df[column].min()) / (
            #     base_df[column].max() - base_df[column].min())
        else:
            base_df[column] = (base_df[column] - base_df[column].mean()) / base_df[column].std()
    base_df['Endurance_Score'] = ""
    for i, rows in base_df.iterrows():
        base_df.loc[i, 'Endurance_Score'] = rows['Popularity'] + rows['Youtube viewcount']
    base_df['Endurance_Score'] = (base_df['Endurance_Score'] - base_df['Endurance_Score'].min()) / (
        base_df['Endurance_Score'].max() - base_df['Endurance_Score'].min())
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'normalized_final_dataset'), index=False)

if __name__ == '__main__':
    # run()
    # update_date()
    # merge_start_date()
    # process_age_distribution()
    normalized_data()
