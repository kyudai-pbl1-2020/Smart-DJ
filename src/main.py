import numpy as np
import pandas as pd
from . import csv2dataset
from . import model_build

#データの読み込み
df = csv2dataset.dataframe_exporter("weather_data/*") 
data = df.drop("weather",axis=1)
target = df["weather"]

model_build.build(data,target)

