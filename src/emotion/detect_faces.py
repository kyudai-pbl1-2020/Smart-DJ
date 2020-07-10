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
        #顔部分を切り取り
        for (x, y, h, w) in facerect:
            face_img = img[y:y+h,x:x+w]
            face_list.append(face_img) 
        #画像のリサイズ
        width,height=64,64
        face_list2=[]
        for face in face_list:
            face = cv2.resize(face,(width,height))
            face_list2.append(face) 
        return face_list2
    else :
        return False      


