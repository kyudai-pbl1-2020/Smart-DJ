import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lightgbm as lgb
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import optuna
from . import csv2dataset

 
#モデルの構築
def build(data,target): 
    
    #ハイパラメータのチューニング
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100)
 
    print('Number of finished trials:', len(study.trials))
    print('Best trial:', study.best_trial.params)

    """
    #ハイパラメータ設定
    params ={}
    
    
    #4foldsでモデルを評価
    scores = []
    kf = Kfold(n_splits=4,shuffle=True,random_state=71)
    for tr_idx, val_idx in kf.split(data):
        tr_x,val_x = data.iloc[tr_idx], data.iloc[val_idx]
        tr_y,val_y = target.iloc[tr_idx], target.iloc[val_idx]
        dtrain = lgb.Dataset(tr_x, label=tr_y)

        gbm = lgb.train(params, dtrain)
        preds = gbm.predict(val_x)
        pred_labels = np.rint(preds)
        score = accuracy_score(va_y,va_pred)
        scores.append(score)

    #データ全体を使って学習
    all_train = lgb.Dataset(data, label=target)
    gbm = lgb.train(params, all_train)
    """


#パラメータのチューニング
def objective(trial):

    #データの読み込み
    df = csv2dataset.dataframe_exporter("weather_data/*") 
    data = df.drop("weather",axis=1)
    target = df["weather"]
    train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25)
    dtrain = lgb.Dataset(train_x, label=train_y)
 
    param = {
        'objective': 'multiclass',
        'metric': 'multi_logloss',
        'lambda_l1': trial.suggest_loguniform('lambda_l1', 1e-8, 10.0),
        'lambda_l2': trial.suggest_loguniform('lambda_l2', 1e-8, 10.0),
        'num_leaves': trial.suggest_int('num_leaves', 2, 256),
        'feature_fraction': trial.suggest_uniform('feature_fraction', 0.4, 1.0),
        'bagging_fraction': trial.suggest_uniform('bagging_fraction', 0.4, 1.0),
        'bagging_freq': trial.suggest_int('bagging_freq', 1, 7),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
    }
 
    gbm = lgb.train(param, dtrain)
    preds = gbm.predict(test_x)
    pred_labels = np.rint(preds)
    accuracy = accuracy_score(test_y, pred_labels)
    return accuracy