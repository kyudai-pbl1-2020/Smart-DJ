import numpy as np
import pandas as pd
#from . import csv2dataset 
#from . import model_build
#import csv2dataset

from weather import csv2dataset
from weather import model_build
from weather import pred
from sensor import sensor_data_processor as sdp
#import tweet

# print(sdp.subscribe_sensor_data())

#データの読み込み
df = csv2dataset.dataframe_exporter("./weather/weather_data/*") 
df = csv2dataset.convert_weather(df,"./weather/convert_weather_token.CSV")
data = df.drop("weather",axis=1)
target = df["weather"]

#モデルの構築
model_build.build(data,target)

#予測用データ読み込み
#pred_data = tanaka.tanaka()

#予測
#pred = pred.pred(pred_data)
#key = np.argmax(pred)

#tweet.tweet(key)