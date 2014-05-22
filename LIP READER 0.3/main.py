#!/usr/bin/env python
import threading
from threading import Thread, Timer
import time
from multiprocessing import Process
import time
import sys, os, gobject
from Tkinter import *
import pygst
pygst.require("0.10")
import gst
import Tkinter as tk
import numpy , Image
import cv2
#import fd2n
import os.path
#from PIL import Image
from PIL import ImageTk, Image
#import cv2
from scipy.misc import toimage
import cv2.cv as cv #Opencv
from PIL import Image #Image from PIL
import glob
import os
script_dir = os.path.dirname(os.path.abspath('gui'))
#camera = cv2.VideoCapture(0)
g=0
h=0
m=1
 

def DetectFace(image, faceCascade, returnImage=False):
    # This function takes a grey scale cv image and finds
    # the patterns defined in the haarcascade function
    # modified from: http://www.lucaamore.com/?p=638

    #variables    
    min_size = (30,30)
    #image_scale = 2
    haar_scale = 1.1
    min_neighbors = 2
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
    
    faceCascade = cv.Load('haarcascade_frontalface_alt.xml')
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
            m=1
            for face in faces:
                croppedImage=imgCrop(pil_im, face[0],boxScale=boxScale)
                croppedImage.save("testdata/face"+str(g)+".jpg")
	        print 1
                mouthcrop = mouthCrop("testdata/face"+str(g)+".jpg",boxScale=1)
		print 2
                g=g+1
		  
		if m==1:
			
			break
                                                
        else:
            print 'No faces found:', img

def mouthCrop(imagePattern,boxScale=1):

    mouthCascade = cv.Load('mouth.xml')
    imgList=glob.glob(imagePattern)
    if len(imgList)<=0:
        print 'No Images Found'
        return
    global h
    for img in imgList:
        pil_im=Image.open(img)
        cv_im=pil2cvGrey(pil_im)
        lips=DetectFace(cv_im,mouthCascade)
        n=1
        size=88,53
        if lips:
            
            for lip in lips:
                croppedImage=imgCrop(pil_im, lip[0],boxScale=boxScale)
                croppedImage=croppedImage.resize(size)
                croppedImage.save("testdata/word/""mouth"+str(h)+".jpg")
                h=h+1
	   
	        if(n==1):      
         	  break
		                             
        else:
            print 'No lips found:', img


# Goto GUI Class
class Prototype(Frame):
    
    def __init__(self, parent):
        
	gobject.threads_init()
        Frame.__init__(self, parent)    
	
        # Parent Object
        self.parent = parent
        self.parent.title("Lip Reader")
        self.parent.geometry("840x640+0+0")
        self.parent.resizable(width=FALSE, height=FALSE)

        # Video Box
        self.movie_window = Canvas(self, width=640, height=440, bg="black")
        self.movie_window.pack(side=TOP, expand=YES, fill=BOTH)

        # Buttons Box
        self.ButtonBox = Frame(self, relief=RAISED, borderwidth=1)
        self.ButtonBox.pack(side=BOTTOM, expand=YES, fill=BOTH)

        self.closeButton = Button(self.ButtonBox, text="Close", command=self.quit)
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)

	self.proButton = Button(self.ButtonBox, text="Process", command=self.process)
        self.proButton.pack(side=RIGHT, padx=5, pady=5)

        self.gotoButton = Button(self.ButtonBox, text="Start", command=self.start_stop)
        self.gotoButton.pack(side=LEFT, padx=5, pady=5)

	self.textBox=Label(text="** Speak")
	self.textBox.pack(side=BOTTOM,padx=20,pady=25)

	
	self.player = gst.parse_launch ("v4l2src ! tee name=t ! queue ! xvimagesink t. ! queue ! videorate ! video/x-raw-yuv, width=640, height=480, framerate=2/1 ! jpegenc ! multifilesink location=testdata/%05d.jpg  ")
	
	print "started"
	bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def process(self):
	i=0
	while True:	 
	     try:

		print i
		print "wait"
		
		pil_im=Image.open('testdata/{0:05d}.jpg'.format(i))

		pil_im.save('testdata/res'+str(i)+'.jpg')
		print "frame saved"
		
		facecrop = mouthCrop('testdata/res'+str(i)+'.jpg',boxScale=1)
		print "mouth croped"
		i += 1
		
             except IOError:
		    break
        print "loop excited"
    	os.system("""sh run.sh """)

	f=open('output.txt','r')
        word=f.read()

	self.textBox['text']=word

	f.close()
		    
    def start_stop(self):
	
	
	if self.gotoButton["text"] == "Start":
           self.gotoButton["text"] = "Stop"
	   self.player.set_state(gst.STATE_PLAYING)
	   print "started playing"
	
	
        else:
	# Release everything if job is finished
           
	   self.gotoButton["text"] = "Start"
	   self.player.set_state(gst.STATE_NULL)
	   self.textBox['text']='** Process '


    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.button.set_label("Start")
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)
            self.button.set_label("Start")

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            # Assign the viewport
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            #imagesink.set_xwindow_id(self.movie_window.window.xid)
	    imagesink.set_xwindow_id(self.movie_window.winfo_id())



def main():

    root=Tk()      
    app = Prototype(root)
    app.pack(expand=YES, fill=BOTH)    
    
    root.mainloop()  

camera = cv2.VideoCapture()



if __name__ == '__main__':
     main()


