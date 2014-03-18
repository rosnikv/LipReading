import numpy as np
import cv2
from PIL import Image
 
im = cv2.imread("mm.jpg")
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,157,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print list(contours)
#print '[%s]' % ', '.join(map(str, contours))
cv2.drawContours(imgray,contours,-1,(0,255,0),-1)
img = Image.fromarray(imgray)
img.save("contourtest.jpg")
