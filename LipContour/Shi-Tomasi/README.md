               OpenCV has a function, cv2.goodFeaturesToTrack(). It finds N strongest corners in the image by Shi-Tomasi method As usual, image should be a grayscale image. Then we specify number of corners you want to find. Then you specify the quality level, which is a value between 0-1, which denotes the minimum quality of corner below which everyone is rejected. Then we provide the minimum euclidean distance between corners detected.
              With all these informations, the function finds corners in the image. All corners below quality level are rejected. Then it sorts the remaining corners based on quality in the descending order. Then function takes first strongest corner, throws away all the nearby corners in the range of minimum distance and returns N strongest corners.

Problem :

*We mainly focus to get 4 points in lip image i.e., left , right , upper and lower. But out of these only left and right points are strong corner points. Since this method tries to find strongest corner points , though we specify the no of corners we want to find as 4 it is not able to find out the upper and lower points. 
(from deepthi's exploration)
