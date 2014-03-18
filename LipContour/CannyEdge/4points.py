import cv2
import numpy as np
import scipy
from PIL import Image



def CannyThreshold(lowThreshold):

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    
    detected_edges = cv2.GaussianBlur(gray,(5,5),0)
    detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
    dst = cv2.bitwise_and(img,img,mask = detected_edges)  # just add some colours to edges from original image.
    #cv2.imshow('canny demo',dst)
    #save numpy.ndarray as image
    im = Image.fromarray(dst)
    im.save("mm.jpg")
    
    closing = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('canny demo',closing)

lowThreshold = 0
max_lowThreshold = 100
ratio = 2
kernel_size = 3

img = cv2.imread('mouth.jpg')
img = cv2.resize(img, (0,0), fx=1.5, fy=1.5) 
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.namedWindow('canny demo')
#THRESHOLD 25 IS BEST
cv2.createTrackbar('Min threshold','canny demo',lowThreshold, max_lowThreshold, CannyThreshold)

CannyThreshold(0)  # initialization
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
