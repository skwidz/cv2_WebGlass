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
    	glasses = cv2.imread("glasses.png", flags=cv2.IMREAD_UNCHANGED)
    	glasses = self.overlayGlasses(glasses)
    	gheight, gwidth, _ = glasses.shape
    	
    	while(1):
    		self.placing = True
    		frame2 = frame.copy()
    		# frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2BGRA)
    	
    		
    		frame2[self.yoff+1: self.yoff+1+gheight, self.xoff+1: self.xoff+1+gwidth] = glasses
    		win.showImage(frame2)
    		if cv2.waitKey(1) & 0xFF == ord('f'):
    			self.placing = False
    			break


    def overlayGlasses(self,overlay):
    	mask = np.zeros_like(overlay)
    	mask = mask[:,:,3:]
    	ov = overlay[:,:,:3]
    	ovmask = overlay[:,:,3:]
    	bgmask = 255 - ovmask
    	ovmask = cv2.cvtColor(ovmask, cv2.COLOR_GRAY2BGR)
    	bgmask = cv2.cvtColor(bgmask, cv2.COLOR_GRAY2BGR)

    	maskpart =  (mask * (1/255.0)) * (bgmask * (1/255.0))
    	overlaypart = (ov * (1/255.0)) * (ovmask * (1/255.0))

    	im = cv2.addWeighted(maskpart, 255.0, overlaypart, 255.0, 0.0)
    	return im

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
