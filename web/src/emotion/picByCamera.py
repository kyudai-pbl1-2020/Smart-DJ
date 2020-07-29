#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import time


# In[10]:


def getImage(path,second):#set saving path and interval time
    index=1
    cap=cv2.VideoCapture(0)
    flag = cap.isOpened()
    while (flag):
        ret,frame = cap.read()
        cv2.imshow("Capture_Paizhao",frame)
        k = cv2.waitKey(1) & 0xFF
        if k==ord('s'):#press s to stop
            break
        else:
            time.sleep(second)
            direciton='%s%d.jpg'%(path,index)
            cv2.imwrite(direciton,frame)
            index+=1
            print('done...')
    cap.release()
    cv2.destroyAllWindows()


# In[12]:


if __name__ == '__main__':
    getImage('G:\photos',10)


# In[ ]:




