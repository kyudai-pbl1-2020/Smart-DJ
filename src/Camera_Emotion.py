#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import matplotlib.pyplot as plt
import time
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import tensorflowjs as tfjs


# In[3]:


def detect(img):

    # 分類器の読込
    cascade_path = 'C:/Users/Administrator.DESKTOP-0E84885/Documents/Smart-DJ-master/src/haarcascade_frontalface_alt.xml'
    
    # グレースケールに変換(顔検用)
    gry_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # カスケード検出器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    
    # 顔検出の実行
    facerect = cascade.detectMultiScale(gry_img, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))

    # 顔画像用リスト


    # 顔を検出した場合
    if len(facerect) > 0:   
        #顔部分を切り取り
        for (x, y, h, w) in facerect:
            face_img = img[y:y+h,x:x+w]

        #画像のリサイズ
        width,height=60,60
        face = cv2.resize(face_img,(width,height))
        return face
    else :
        return False  


# In[4]:


def key_func(n):
    return n[1]

def emotion_recognition(image_path): #predict emotion from image of 
    classes = ({0:'angry',1:'disgust',2:'fear',3:'happy',
            4:'sad',5:'surprise',6:'neutral'})

    img = image.load_img(image_path, grayscale=True , target_size=(64, 64))  #get face image
    img_array = image.img_to_array(img)  #convert to array
    pImg = np.expand_dims(img_array, axis=0) / 255

    model_path = './trained_models/fer2013_mini_XCEPTION.110-0.65.hdf5'  #get path of trained model

    emotions_XCEPTION = load_model(model_path, compile=False)  #build model

    prediction = emotions_XCEPTION.predict(pImg)[0]  #predict emotion

    top_indices = prediction.argsort()[-5:][::-1]
    result = [(classes[i] , prediction[i]) for i in top_indices]
    emotion_max = max(result, key=key_func)  #get strongest emotion
    label = emotion_max[0]
    return label


# In[5]:


def getEmotion(path,second):#set saving path and interval time
    index=1
    cap=cv2.VideoCapture(0)
    flag = cap.isOpened()
    width=64
    height=64
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    while (flag):
        ret,frame = cap.read()
        cv2.imshow("Capture_Paizhao",frame)
        k = cv2.waitKey(1) & 0xFF
        if k==ord('s'):#press s to stop
            break
        else:
            
            direction='%sphoto%d.jpg'%(path,index)             
            cv2.imwrite(direction,frame)
            #face detect
            img_BGR=cv2.imread(direction)
            face=detect(img_BGR)
            direction2='%stest%d.jpg'%(path,index) 
            cv2.imwrite(direction2,face)
            
            #emotion predict
            label =  emotion_recognition(direction2)
            
            print("the %d picture is %s"%(index,label))
            
            index+=1
            
            
            time.sleep(second)
            
            
    cap.release()
    cv2.destroyAllWindows()
    return label


# In[ ]:


#input the direction of image that you want to save.There will save a original picture and 64*64 picture.
#it takes photos every 30min
getEmotion('G:/',30)


# In[ ]:




