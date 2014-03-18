import numpy
import cv2
#import fd2n
#from PIL import Image
#import cv2
import cv2.cv as cv #Opencv
from PIL import Image #Image from PIL
import glob
import os
g=0
def DetectFace(image, faceCascade, returnImage=False):
    # This function takes a grey scale cv image and finds
    # the patterns defined in the haarcascade function
    # modified from: http://www.lucaamore.com/?p=638

    #variables    
    min_size = (30,30)
    #image_scale = 2
    haar_scale = 1.1
    min_neighbors = 1
    haar_flags = 0

    # Equalize the histogram
    cv.EqualizeHist(image, image)

    # Detect the faces
    faces = cv.HaarDetectObjects(
            image, faceCascade, cv.CreateMemStorage(0),
            haar_scale, min_neighbors, haar_flags, min_size
        )

    # If faces are found
    if faces and returnImage:
        for ((x, y, w, h), n) in faces:
            # Convert bounding box to two CvPoints
            pt1 = (int(x), int(y))
            pt2 = (int(x + w), int(y + h))
            cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 5, 8, 0)

    if returnImage:
        return image
    else:
        return faces

def pil2cvGrey(pil_im):
    # Convert a PIL image to a greyscale cv image
    # from: http://pythonpath.wordpress.com/2012/05/08/pil-to-opencv-image/
    pil_im = pil_im.convert('L')
    cv_im = cv.CreateImageHeader(pil_im.size, cv.IPL_DEPTH_8U, 1)
    cv.SetData(cv_im, pil_im.tostring(), pil_im.size[0]  )
    return cv_im

def cv2pil(cv_im):
    # Convert the cv image to a PIL image
    return Image.fromstring("L", cv.GetSize(cv_im), cv_im.tostring())

def imgCrop(image, cropBox, boxScale=1):
    # Crop a PIL image with the provided box [x(left), y(upper), w(width), h(height)]

    # Calculate scale factors
    xDelta=max(cropBox[2]*(boxScale-1),0)
    yDelta=max(cropBox[3]*(boxScale-1),0)

    # Convert cv box to PIL box [left, upper, right, lower]
    PIL_box=[cropBox[0]-xDelta, cropBox[1]-yDelta, cropBox[0]+cropBox[2]+xDelta, cropBox[1]+cropBox[3]+yDelta]

    return image.crop(PIL_box)

def faceCrop(imagePattern,boxScale=1):
    # Select one of the haarcascade files:
    #   haarcascade_frontalface_alt.xml  <-- Best one?
    #   haarcascade_frontalface_alt2.xml
    #   haarcascade_frontalface_alt_tree.xml
    #   haarcascade_frontalface_default.xml
    #   haarcascade_profileface.xml
    faceCascade = cv.Load('mouth.xml')
    imgList=glob.glob(imagePattern)
    if len(imgList)<=0:
        print 'No Images Found'
        return
    global g
    for img in imgList:
        pil_im=Image.open(img)
        cv_im=pil2cvGrey(pil_im)
        faces=DetectFace(cv_im,faceCascade)
        if faces:
            n=1
            for face in faces:
                croppedImage=imgCrop(pil_im, face[0],boxScale=boxScale)
                croppedImage.save("mouth"+str(g)+".jpg")
                g=g+1
		if n==1:
			break
                
                
                
        else:
            print 'No faces found:', img


#MAIN METHOD
camera = cv2.VideoCapture(0)
i = 0
while True:
	f,img = camera.read()
	im = numpy.array(img)
	cv2.imshow("webcam",im)
	if (cv2.waitKey(5) != -1):
		break
	
	cv2.imwrite('{0:05d}.jpg'.format(i),im)
	pil_im=Image.open('{0:05d}.jpg'.format(i))
	#fname,ext=os.path.splitext(pil_im)
	pil_im.save('res'+str(i)+'.jpg')
	
	facecrop = faceCrop('res'+str(i)+'.jpg',boxScale=1)

	i += 1


# Release everything if job is finished
camera.release()
out.release()
cv2.destroyAllWindows()

