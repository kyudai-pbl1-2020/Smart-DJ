import cv2
import matplotlib.pyplot as plt

def detect(img):

    # 分類器の読込
    cascade_path = './haarcascade_frontalface_alt.xml'
    
    # グレースケールに変換(顔検用)
    gry_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # カスケード検出器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    
    # 顔検出の実行
    facerect = cascade.detectMultiScale(gry_img, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))

    # 顔画像用リスト
    face_list = []

    # 顔を検出した場合
    if len(facerect) > 0:   
        for (x, y, h, w) in facerect:
            face_img = img[y:y+h,x:x+w]
            face_list.append(face_img) 
    
    return face_list         
