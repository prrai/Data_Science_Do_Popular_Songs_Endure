import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

path_final_csv = r'../data/final/experiments'


def run():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'entry_distance_range_1_21'), encoding='latin-1')
    base_df['diff'] = ""
    for i, row in base_df.iterrows():
        base_df.loc[i, 'diff'] = row.expected - row.predicted
    base_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'entry_distance_range_1_21'), index=False)


def plot_75_100():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'peak_position_range_75_100'), encoding='latin-1')
    y = list()
    x = list()
    ctr = 0
    for i, rows in base_df.iterrows():
        if rows.expected > 0.80:
            y.append(rows['diff'])
            x.append(ctr)
            ctr += 1
    axes = plt.gca()
    axes.set_ylim([-1.0, 1.0])
    plt.scatter(x, y, s=1.5)
    plt.ylabel("Difference in predicted vs expected endurance score")
    plt.xlabel("Sample instance")
    plt.show()


def plot_1_25():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'peak_position_range_1_25'), encoding='latin-1')
    y = list()
    x = list()
    ctr = 0
    for i, rows in base_df.iterrows():
        if rows.expected < 0.65:
            y.append(rows['diff'])
            x.append(ctr)
            ctr += 1
    axes = plt.gca()
    axes.set_ylim([-1.0, 1.0])
    plt.scatter(x, y, s=1.5)
    plt.ylabel("Difference in predicted vs expected endurance score")
    plt.xlabel("Sample instance")
    plt.show()


def plot_entry_45_150():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'entry_distance_range_45_150'), encoding='latin-1')
    y = list()
    x = list()
    ctr = 0
    for i, rows in base_df.iterrows():
        if rows.expected > 0.80:
            y.append(rows['diff'])
            x.append(ctr)
            ctr += 1
    axes = plt.gca()
    axes.set_ylim([-1.0, 1.0])
    plt.scatter(x, y, s=1.5)
    plt.ylabel("Difference in predicted vs expected endurance score")
    plt.xlabel("Sample instance")
    plt.show()


def plot_entry_1_21():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'entry_distance_range_1_21'), encoding='latin-1')
    y = list()
    x = list()
    ctr = 0
    for i, rows in base_df.iterrows():
        if rows.expected < 0.65:
            y.append(rows['diff'])
            x.append(ctr)
            ctr += 1
    axes = plt.gca()
    axes.set_ylim([-1.0, 1.0])
    plt.scatter(x, y, s=1.5)
    plt.ylabel("Difference in predicted vs expected endurance score")
    plt.xlabel("Sample instance")
    plt.show()


def get_R2_and_RMSE():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'peak_position_range_1_25'), encoding='latin-1')
    y_test = base_df['expected']
    y_pred = base_df['predicted']
    rmse = mean_squared_error(y_test, y_pred)
    score = r2_score(y_test, y_pred)
    print("R2-score: {}, RMSE: {}".format(score, math.sqrt(rmse)))


def plot_feature_distribution():
    df = pd.read_csv('{0}/../{1}.csv'.format(path_final_csv, 'predicted_finaldata'), encoding='latin-1')
    df = df.drop(df[(df.Endurance_Score >= 0.65)].index)
    df = df.drop(df[(df.days_before_charting < 1)].index)
    df = df.drop(df[(df.days_before_charting > 21)].index)

    df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'filtered_data_entry_1_21'), index=False)



if __name__ == '__main__':
    # run()
    # plot_75_100()
    # plot_1_25()
    # plot_entry_45_150()
    # plot_entry_1_21()
    # get_R2_and_RMSE()
    plot_feature_distribution()

