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

path_final_csv = r'../data/'


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
    result_df['Endurance_Score'] = y_test.ravel()
    result_df['Predicted_Endurance_Score'] = y_pred
    result_df.to_csv('{0}/{1}.csv'.format(path_final_csv, 'predicted_midtermdata'), index=False)


def run():
    base_df = pd.read_csv('{0}/{1}.csv'.format(path_final_csv, 'normalized_midtermdata'), encoding='latin-1')
    test_frame = base_df.copy()
    column_list = list(base_df)
    column_list.remove('Youtube viewcount')
    column_list.remove('Popularity')
    column_list.remove('Endurance_Score')
    model = 'ridge'
    print("Evaluating for the model: {}".format(model))
    run_specific_combination(test_frame, model, column_list)

if __name__ == '__main__':
    run()
