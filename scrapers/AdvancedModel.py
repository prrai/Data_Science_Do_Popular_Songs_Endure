import os
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from collections import defaultdict
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn import cluster as Kcluster, metrics as SK_Metrics
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor, ExtraTreesRegressor
from sklearn import gaussian_process
from sklearn import kernel_ridge
from sklearn import neighbors
from sklearn import svm
from itertools import combinations

path_final_csv = r'../data/final'


def run_specific_combination(test_frame, reg_type, column_list):
    target_feature = test_frame['Endurance_Score']
    test_df = test_frame.filter(column_list, axis=1)
    X_train, X_test, y_train, y_test = train_test_split(
                test_df, target_feature.values.reshape(-1,1),
                test_size=0.20, random_state=0)
    if reg_type == 'dt':
        regr = DecisionTreeRegressor(max_depth=2)
    elif reg_type == 'lin':
        regr = linear_model.LinearRegression()
    elif reg_type == 'ridge':
        regr = linear_model.Ridge(alpha=1500.0)
    elif reg_type == 'lasso':
        regr = linear_model.Lasso(alpha=10.0)
    elif reg_type == 'bayridge':
        regr = linear_model.BayesianRidge()
    elif reg_type == 'sgd':
        regr = linear_model.SGDRegressor(loss='huber')
    elif reg_type == 'lars':
        regr = linear_model.Lars(n_nonzero_coefs=np.inf)
    elif reg_type == 'pasagv':
        regr = linear_model.PassiveAggressiveRegressor(random_state=0)
    elif reg_type == 'kernelridge':
        regr = kernel_ridge.KernelRidge()
    elif reg_type == 'svr':
        regr = svm.SVR()
    elif reg_type == 'kneigh':
        regr = neighbors.KNeighborsRegressor(algorithm='kd_tree')
    elif reg_type == 'gauss':
        regr = gaussian_process.GaussianProcessRegressor()
    elif reg_type == 'gbr':
        params = {'n_estimators': 760, 'max_depth': 4, 'min_samples_split': 3, 'learning_rate': 0.026, 'loss': 'huber'}
        regr = GradientBoostingRegressor(**params)
    elif reg_type == 'ran':
        regr = RandomForestRegressor(n_estimators=300, max_depth=8)
    elif reg_type == 'et':
            regr = ExtraTreesRegressor()
    else:
        return
    x_train_frame = X_train.copy()
    del x_train_frame['Title']
    del x_train_frame['Artist']
    regr.fit(x_train_frame, y_train.ravel())
    x_test_frame = X_test.copy()
    del x_test_frame['Title']
    del x_test_frame['Artist']
    y_pred = regr.predict(x_test_frame)
    rmse = mean_squared_error(y_test, y_pred)
    score = r2_score(y_test, y_pred)
    print("R2-score: {}, RMSE: {}".format(score, math.sqrt(rmse)))
    result_df = pd.DataFrame(columns=['Song', 'Artist', 'Endurance_Score', 'Predicted_Endurance_Score'])
    result_df['Song'] = X_test['Title']
    result_df['Artist'] = X_test['Artist']
    ###
    result_df['Entry_Position'] = ""
    result_df['Peak_Position'] = ""
    result_df['Total_Weeks'] = ""
    result_df['danceability'] = ""
    result_df['energy'] = ""
    result_df['key'] = ""
    result_df['loudness'] = ""
    result_df['mode'] = ""
    result_df['speechiness'] = ""
    result_df['acousticness'] = ""
    result_df['instrumentalness'] = ""
    result_df['liveness'] = ""
    result_df['valence'] = ""
    result_df['tempo'] = ""
    result_df['duration_ms'] = ""
    result_df['time_signature'] = ""
    result_df['Movies_TV_feature_count'] = ""
    result_df['Oscars_won'] = ""
    result_df['Artist_lifetime_grammy_achievement'] = ""
    result_df['Artist_grammy_wins'] = ""
    result_df['Artist_grammy_nominations'] = ""
    result_df['artist popularity'] = ""
    result_df['TopSongsArtist'] = ""
    result_df['TopSongsArtist10'] = ""
    result_df['TopSongsArtist100'] = ""
    result_df['Entry_Year'] = ""
    result_df['days_before_charting'] = ""
    result_df['Age_Percentage_15_30'] = ""

    ###

    result_df['Endurance_Score'] = y_test.ravel()
    result_df['Predicted_Endurance_Score'] = y_pred
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'final_unnormalized_dataset'), encoding='latin-1')
    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Entry_Position

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Entry_Position'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Peak_Position

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Peak_Position'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Total_Weeks

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Total_Weeks'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.danceability

    for i, row in result_df.iterrows():
        result_df.loc[i, 'danceability'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.energy

    for i, row in result_df.iterrows():
        result_df.loc[i, 'energy'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.key

    for i, row in result_df.iterrows():
        result_df.loc[i, 'key'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.loudness

    for i, row in result_df.iterrows():
        result_df.loc[i, 'loudness'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.mode

    for i, row in result_df.iterrows():
        result_df.loc[i, 'mode'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.speechiness

    for i, row in result_df.iterrows():
        result_df.loc[i, 'speechiness'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.acousticness

    for i, row in result_df.iterrows():
        result_df.loc[i, 'acousticness'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.instrumentalness

    for i, row in result_df.iterrows():
        result_df.loc[i, 'instrumentalness'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.liveness

    for i, row in result_df.iterrows():
        result_df.loc[i, 'liveness'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.valence

    for i, row in result_df.iterrows():
        result_df.loc[i, 'valence'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.tempo

    for i, row in result_df.iterrows():
        result_df.loc[i, 'tempo'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.duration_ms

    for i, row in result_df.iterrows():
        result_df.loc[i, 'duration_ms'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.time_signature

    for i, row in result_df.iterrows():
        result_df.loc[i, 'time_signature'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Movies_TV_feature_count

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Movies_TV_feature_count'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Oscars_won

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Oscars_won'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Artist_lifetime_grammy_achievement

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Artist_lifetime_grammy_achievement'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Artist_grammy_wins

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Artist_grammy_wins'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Artist_grammy_nominations

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Artist_grammy_nominations'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row['artist popularity']

    for i, row in result_df.iterrows():
        result_df.loc[i, 'artist popularity'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.TopSongsArtist

    for i, row in result_df.iterrows():
        result_df.loc[i, 'TopSongsArtist'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.TopSongsArtist10

    for i, row in result_df.iterrows():
        result_df.loc[i, 'TopSongsArtist10'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.TopSongsArtist100

    for i, row in result_df.iterrows():
        result_df.loc[i, 'TopSongsArtist100'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Entry_Year

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Entry_Year'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.days_before_charting

    for i, row in result_df.iterrows():
        result_df.loc[i, 'days_before_charting'] = results[row.Song]
    ####-----------------------------------------------###

    ####-----------------------------------------------###
    results = dict()
    for i, row in base_df.iterrows():
        results[row.Title] = row.Age_Percentage_15_30

    for i, row in result_df.iterrows():
        result_df.loc[i, 'Age_Percentage_15_30'] = results[row.Song]
    ####-----------------------------------------------###

    result_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'predicted_finaldata'), index=False)


def run():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'normalized_final_dataset'), encoding='latin-1')
    test_frame = base_df.copy()
    column_list = list(base_df)
    column_list.remove('Youtube viewcount')
    column_list.remove('Popularity')
    column_list.remove('Endurance_Score')
    column_list.remove('Entry_Date')
    column_list.remove('release_date')
    model = 'gbr'
    print("Evaluating for the model: {}".format(model))
    run_specific_combination(test_frame, model, column_list)

if __name__ == '__main__':
    run()
