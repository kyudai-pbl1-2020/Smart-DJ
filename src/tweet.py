import json, config_tw #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
import pred

def tweet(data):

    CK = config_tw.CONSUMER_KEY
    CS = config_tw.CONSUMER_SECRET
    AT = config_tw.ACCESS_TOKEN
    ATS = config_tw.ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

    url = "https://api.twitter.com/1.1/statuses/update.json" #ツイートポストエンドポイント

    weather = ["#sunny","#cloud","#rainy"]
    key = pred.predict(data)
    #key = 0
    tweet = weather[key]

    params = {"status" : tweet}

    res = twitter.post(url, params = params) #post送信

    if res.status_code == 200: #正常投稿出来た場合
        print("Success.")
    else: #正常投稿出来なかった場合
        print("Failed. : %d"% res.status_code)

