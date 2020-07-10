from flask import Flask, jsonify, request
import json
import numpy as np
import pandas as pd
import requests
from weather import csv2dataset
from weather import model_build
from weather import pred
from sensor import sensor_data_processor as sdp
from emotion import emotionmain as em


app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "route get. Hello!"

@app.route('/reply', methods=['POST'])
def reply():
    data = json.loads(request.data)
    answer = "route post. keyword is %s!\n" % data["keyword"]
    result = {
      "Content-Type": "application/json",
      "Answer":{"Text": answer}
    }
    # return answer
    return jsonify(result)

@app.route("/sensor")
def sensor():
    df = csv2dataset.dataframe_exporter("./weather/weather_data/*") 
    df = csv2dataset.convert_weather(df,"./weather/convert_weather_token.csv")
    data = df.drop("weather",axis=1)
    target = df["weather"]

    #モデルの構築
    #model_build.build(data,target)

    #予測用データ読み込み (list['month','hour','temperature','pressure','humidity'])
    pred_data = sdp.subscribe_sensor_data()
    #pred_data = [6,17,27.12,998.2,64.22] #テスト用
    #print(pred_data)
    #予測データの変換

    if len(pred_data) != 0:
        pred_data = pd.Series(pred_data, index=['month','hour','temperature','pressure','humidity'])
        keyword = pred.pred(pred_data)
        #label = 'test'
        #key = ''
        #requests.get('https://maker.ifttt.com/trigger/' + label + '/with/key/' + key)

        return(str(keyword) + 'sensor')

@app.route("/img")
    emo = em.emotion()


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)