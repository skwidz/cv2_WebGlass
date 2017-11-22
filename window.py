import cv2
import numpy as np
import random


class Window:

    def __init__(self):
        self.windowName = str(random.random())
        cv2.namedWindow(self.windowName)
        cv2.setMouseCallback(self.windowName, self.mousecallback)
        self.xoff = 0
        self.xinit = 0
        self.yoff = 0
        self.yinit = 0
        self.dragging = False
        self.placing = False
        # cv2.resizeWindow(self.windowName, 600, 600)

    def showImage(self, image):
        cv2.imshow(self.windowName, image)

    def destroy(self):
        cv2.destroyWindow(self.windowName)

    def placeGlasses(self,cam, win):
    	frame = cam.getNewFrame()
    	glasses = cv2.imread("glasses.png")
    	gheight, gwidth, _ = glasses.shape
    	
    	while(1):
    		self.placing = True
    		frame2 = frame.copy()
    		frame2[self.yoff+1: self.yoff+1+gheight, self.xoff+1: self.xoff+1+gwidth] = glasses
    		win.showImage(frame2)
    		if cv2.waitKey(1) & 0xFF == ord('f'):
    			self.placing = False
    			break


    def warpGlasses(self, frame, points):
    	return true 


    def mousecallback(self,event, x,y, flags, params):
    	if self.placing:
	    	if event == cv2.EVENT_LBUTTONDOWN:
	    		self.dragging = True
	    		self.xinit = x
	    		self.yinit = y
	    	elif event == cv2.EVENT_MOUSEMOVE:
	    		if self.dragging == True:
	    			self.xoff = (x - self.xinit)
	    			self.yoff = (y - self.yinit)
	    	elif event == cv2.EVENT_LBUTTONUP:
	    		self.dragging = False
