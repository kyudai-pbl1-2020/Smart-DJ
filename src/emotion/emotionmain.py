import detect_faces as df
import emotion_predict as ep
import cv2
from keras.preprocessing import image

#画像をsampleを開
def emotion():
    img = cv2.imread('images/sad.jpg')

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

    return label