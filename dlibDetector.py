import cv2 
import dlib
from imutils import face_utils
import imutils
import numpy as np

import cameraController as cc
import window as w

# implemented following: https://www.pyimagesearch.com/2017/04/17/real-time-facial-landmark-detection-opencv-python-dlib/
class DlibDetector:
	def __init__(self):
		print('[INFO] Loading facial landmark predictor')
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

	# returns the facial points as an NP array
	def getFacialPointsNP(self,frame):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rects = self.detector(gray, 0)
		# only do one face, the first face, whatever that might be
		shape = []
		for rect in rects[:1]:
			shape = self.predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)
		return shape
				
	# displays the facial points as circles over the 
	def showFacialPoints(self, frame, points):
		for (x,y) in points: #we cont need the jaw points, those start at 17
			cv2.circle(frame, (x,y),1,(0,0,255), -1)
		return frame
