from flask import Flask, jsonify, request,redirect,url_for,flash, render_template
import json
import os 
import numpy as np
import pandas as pd
import requests
from weather import csv2dataset
from weather import model_build
from weather import pred
#from sensor import sensor_data_processor as sdp
from emotion import detect_faces as df
from emotion import emotion_predict as ep
import cv2
from keras.preprocessing import image
from werkzeug.utils import secure_filename
from flask import send_from_directory

import mysql.connector
# Dockerを使う場合で、初期設定の場合hostは"192.168.99.100"
# MySQLのユーザやパスワード、データベースはdocker-compose.ymlで設定したもの




app = Flask(__name__)

# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allwed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET'])
def hello():
    return "route get. Hello!"

@app.route('/db')
def db():
    connector = mysql.connector.connect(
        user='user',
        password='password',
        host='mysql_db',
        database='sample_db',
        port='3306')

    cursor = connector.cursor()
    cursor.execute("select * from users")


    disp = ""
    for row in cursor.fetchall():
        disp = "ID:" + str(row[0]) + "<br>month:" + str(row[1]) + "<br>day:" + str(row[2]) + "<br>temperature:" + str(row[3]) + "<br>pressure:" + str(row[4]) + "<br>humidity:" + str(row[5])

    cursor.close
    connector.close
    return disp

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
    #pred_data = sdp.subscribe_sensor_data()
    pred_data = [6,17,27.12,998.2,64.22] #テスト用
    #print(pred_data)
    #予測データの変換

    if len(pred_data) != 0:
        pred_data = pd.Series(pred_data, index=['month','hour','temperature','pressure','humidity'])
        keyword = pred.pred(pred_data)
        #label = 'test'
        #key = ''
        #requests.get('https://maker.ifttt.com/trigger/' + label + '/with/key/' + key)

        return(str(keyword) + 'sensor')

@app.route("/emotion")
def show_emotion():
    # emotion
    img = cv2.imread('./uploads/sad.jpg')
    face_list =  df.detect(img)

    for i in range(len(face_list)):
        image_path = "faces/"+str(i)+".jpg"
        cv2.imwrite(image_path,face_list[i])

    img_list = []
    for i in range(len(face_list)):
        image_path = "faces/"+str(i)+".jpg"
        img = image.load_img(image_path, grayscale=True , target_size=(64, 64))
        img_list.append(img)

    label = ep.emotion_recognition(img_list)

    # weather
    connector = mysql.connector.connect(
        user='user',
        password='password',
        host='mysql_db',
        database='sample_db',
        port='3306')

    cursor = connector.cursor()
    cursor.execute("select * from users")


    disp = ""
    pred_data = []
    for row in cursor.fetchall():
        disp = "ID:" + str(row[0]) + "<br>month:" + str(row[1]) + "<br>day:" + str(row[2]) + "<br>temperature:" + str(row[3]) + "<br>pressure:" + str(row[4]) + "<br>humidity:" + str(row[5])
        pred_data = [row[1], row[2], row[3], row[4], row[5]]

    cursor.close
    connector.close
    # pred_data = sdp.subscribe_sensor_data()
    # pred_data = [6,17,27.12,998.2,64.22] #テスト用
    pred_data = pd.Series(pred_data, index=['month','hour','temperature','pressure','humidity'])
    keyword = pred.pred(pred_data)
    weather_str = ''
    if (keyword == 0):
        weather_str = 'sunny'
    elif (keyword == 1):
        weather_str = 'cloudy'
    elif (keyword == 2):
        weather_str = 'rainy'
    
    context = {}
    context['label'] = label
    context['weather_str'] = weather_str
    # return 'emotion : ' + str(label[0]) + '<br>weather : ' + str(weather_str)
    return render_template('prediction.html',**context)

@app.route("/up_img", methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        file = request.files['file']
        # ファイル名がなかった時の処理
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        # ファイルのチェック
        if file and allwed_file(file.filename):
            # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
            # ファイルの保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # アップロード後のページに転送
            return redirect(url_for('show_emotion'))
    return render_template("DJ.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)