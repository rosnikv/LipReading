import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


def temp(img1,n):
    
    img = cv2.imread(img1,0)
    img2 = img.copy()
    template = cv2.imread('training_set/template.jpg',0)
    w, h = template.shape[::-1]

    meth='cv2.TM_SQDIFF_NORMED'


    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)  
    
    cr_im=img[top_left[1]:top_left[1]+h,top_left[0]:top_left[0]+w]
    
    cv2.imwrite('testdata/word/'+str(n)+'.jpg',cr_im)
    


