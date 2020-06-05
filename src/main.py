import numpy as np
import pandas as pd
#from . import csv2dataset 
#from . import model_build
import csv2dataset 
import model_build
import pred
import tanaka

#データの読み込み
df = csv2dataset.dataframe_exporter("./weather_data/*") 
data = df.drop("weather",axis=1)
target = df["weather"]

#モデルの構築
model_build.build(data,target)

#予測用データ読み込み
pred_data = tanaka.tanaka()

#予測
pred.pred(pred_data)