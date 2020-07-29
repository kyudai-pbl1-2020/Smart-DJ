import os
import random

def getImage(root_path):
    index=1
    img_list=[]
    dir = root_path+"images"+"/"
    for root,dir,files in os.walk(dir):
        for file in files:
            image_path=root_path+"images"+"/"+str(file)
            srcImg=image.load_img(image_path, grayscale=True , target_size=(64, 64)) 
            img_list.append(srcImg)
            print(index)
            index+=1
    random.shuffle(img_list)
    return img_list



