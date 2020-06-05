import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lightgbm as lgb
from sklearn.metrics import log_loss,accuracy_score
from sklearn.model_selection import train_test_split
import optuna
import pickle
import csv2dataset


 
#モデルの構築
def build(data,target): 
    
    #ハイパラメータのチューニング
    study = optuna.create_study(direction='maximize')
    study.optimize(objective_data(data,target), n_trials=100)
 
    print('Number of finished trials:', len(study.trials))
    print('Best trial:', study.best_trial.params)

    """
    #ハイパラメータ設定
    params = study.best_params
    
    
    #4foldsでモデルを評価
    scores = []
    kf = Kfold(n_splits=4,shuffle=True,random_state=71)
    for tr_idx, val_idx in kf.split(data):
        tr_x,val_x = data.iloc[tr_idx], data.iloc[val_idx]
        tr_y,val_y = target.iloc[tr_idx], target.iloc[val_idx]
        dtrain = lgb.Dataset(tr_x, label=tr_y)

        gbm = lgb.train(params, dtrain)
        preds = gbm.predict(val_x)
        # 最尤と判断したクラスの値にする
        preds_max = np.argmax(preds, axis=1)  
        
        # 精度 (Accuracy) を計算する
        score = sum(val_y == preds_max) / len(val_y)
        scores.append(score)
    print(f'logloss: {np.mean(scores):.4f}')

    #データ全体を使って学習
    all_train = lgb.Dataset(data, label=target)
    gbm = lgb.train(params, all_train)

    #モデルを保存
    file = 'trained_model.pkl'
    pickle.dump(clf, open(file, 'wb'))


    """


#パラメータのチューニング
def objective_data(data,target):
    def objective(trial):

        #データの読み込み
        train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25)
        dtrain = lgb.Dataset(train_x, label=train_y)
    
        param = {
            'objective': 'multiclass',
            'metric': 'multi_logloss',
            'num_class': 16,
            'boosting': 'gbdt',
            'lambda_l1': trial.suggest_loguniform('lambda_l1', 1e-8, 10.0),
            'lambda_l2': trial.suggest_loguniform('lambda_l2', 1e-8, 10.0),
            'num_leaves': trial.suggest_int('num_leaves', 2, 256),
            'feature_fraction': trial.suggest_uniform('feature_fraction', 0.4, 1.0),
            'bagging_fraction': trial.suggest_uniform('bagging_fraction', 0.4, 1.0),
            'bagging_freq': trial.suggest_int('bagging_freq', 1, 7),
            'max_depth' : trial.suggest_int('max_depth', 3, 9),
        }
    
        gbm = lgb.train(param, dtrain)
        preds = gbm.predict(test_x)
        preds_max = np.argmax(preds, axis=1)  
        # 最尤と判断したクラスの値にする
        # 精度 (Accuracy) を計算する
        accuracy = sum(test_y == preds_max) / len(test_y)
        return accuracy
    return objective