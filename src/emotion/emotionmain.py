import detect_faces as df
import emotion_predict as ep
from PIL import Image
#画像をsampleを開く
img = Image.open('images/happy.jpg')

face_list =  df.detect(img)

for i in range(len(face_list)):
    face_list[i].save("faces/"+str(i)+".jpg")

img_list = []
for i in range(len(face_list)):
    img = Image.open("faces/"+str(i)+".jpg")
    
    img_list.append(img)

label = ep.emotion_recognition(img_list)
print(label)