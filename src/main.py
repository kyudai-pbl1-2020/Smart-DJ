import numpy as np
import pandas as pd
from weather import csv2dataset
from weather import model_build
from weather import pred
from sensor import sensor_data_processor as sdp
#import tweet

#データの読み込み
df = csv2dataset.dataframe_exporter("./weather/weather_data/*") 
df = csv2dataset.convert_weather(df,"./weather/convert_weather_token.csv")
data = df.drop("weather",axis=1)
target = df["weather"]

#モデルの構築
#model_build.build(data,target)

#予測用データ読み込み (list['month','hour','temperature','pressure','humidity'])
pred_data = sdp.subscribe_sensor_data()
print(pred_data)
#予測データの変換

if len(pred_data) != 0:
    #pred_data = pd.DataFrame({'month' : pred_data[0], 'hour' : pred_data[1],'temperature' : pred_data[2], 'pressure' : pred_data[3],'humidity':pred_data[4]})
    pred_data = pd.Series(pred_data, index=['month','hour','temperature','pressure','humidity'])
    pred_data2 = pred.pred(pred_data)
    key = np.argmax(pred_data2)

#tweet.twee