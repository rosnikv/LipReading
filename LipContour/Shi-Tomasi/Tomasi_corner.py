import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('mouth.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


corners = cv2.goodFeaturesToTrack(gray,7,0.0001,1)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),1,255,-1)

plt.imshow(img),plt.show()
img.save("out.jpg")
