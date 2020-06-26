import numpy as np
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import tensorflowjs as tfjs

def key_func(n):
    return n[1]

def emotion_recognition(img_list): #predict emotion from image of 
   
    classes = ({0:'angry',1:'disgust',2:'fear',3:'happy',
            4:'sad',5:'surprise',6:'neutral'})
    label_list=[]

    for img in img_list:
        img_array = image.img_to_array(img)  #convert to array
        pImg = np.expand_dims(img_array, axis=0) / 255

        model_path = './trained_models/fer2013_mini_XCEPTION.110-0.65.hdf5'  #get path of trained model

        emotions_XCEPTION = load_model(model_path, compile=False)  #build model

        prediction = emotions_XCEPTION.predict(pImg)[0]  #predict emotion

        top_indices = prediction.argsort()[-5:][::-1]
        result = [(classes[i] , prediction[i]) for i in top_indices]
        emotion_max = max(result, key=key_func)  #get strongest emotion
        label = emotion_max[0]

        label_list.append(label)

    return label_list


def main():
    image_path = './images/happy.jpg'
    label =  emotion_recognition(image_path)
    print(label)

main()

