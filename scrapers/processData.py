import os
import pandas as pd

path_final_csv = r'../data/'


def run():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'midtermdata'), encoding='latin-1')
    base_df = base_df[base_df.Popularity != -1]
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'clean_midtermdata'), index=False)


def update_date():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'clean_midtermdata'), encoding='latin-1')
    for i, rows in base_df.iterrows():
        base_df.loc[i, 'Entry_Date'] = int(base_df['Entry_Date'][i].split('/')[2])
    base_df = base_df[base_df.Entry_Date < 2014]
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_date_midtermdata'), index=False)


def normalized_data():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'updated_date_midtermdata'), encoding='latin-1')
    del base_df['Title']
    del base_df['Artist']
    for column in base_df:
        if column == 'Youtube viewcount':
            base_df[column] /= 2
        base_df[column].fillna((base_df[column].median()), inplace=True)
        if column == 'Youtube viewcount' or column == 'Popularity':
            base_df[column] = (base_df[column] - base_df[column].min()) / (
                base_df[column].max() - base_df[column].min())
        else:
            base_df[column] = (base_df[column] - base_df[column].mean()) / base_df[column].std()
    base_df['Endurance_Score'] = ""
    for i, rows in base_df.iterrows():
        base_df.loc[i, 'Endurance_Score'] = rows['Popularity'] + rows['Youtube viewcount']
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'normalized_midtermdata'), index=False)

if __name__ == '__main__':
    run()
    update_date()
    normalized_data()
