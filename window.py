import cameraController as cc
import cv2
import numpy as np
import random

class Window:

	def __init__(self):
		self.windowName = str(random.random())
		refPoints = np.float32([[[1.0,1.0]]]) # does this really need to be initalised?
		placingRefPoints = False

	def getRefPoints(self):
		return self.refPoints

	def setClickCallback(self, callback):
		cv2.setCallback(self.windowName, callback);
	
	def addPointClick(event, x, y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN & placingRefPoints == True:
			self.refPoints = np.append(self.refPoints,[[[np.float32(x), np.float32(y)]]],axis=0)

	def showImage(self, image):
			cv2.imshow('frame', image)

	def destroy(self):
		cv2.destroyWindow(self.windowName)

cam = cc.CameraController()
cam.getCameraParams()
win = Window()
while(1):
	win.showImage(cam.getNewFrame()) 
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cam.destroy()
		break
