import cv2
import numpy as np

class StructureFromMotion:
	def __init__(self):
		self.initialPoints = []

	def getHomo(self, points):
		homo = cv2.convertPointsToHomogeneous(np.array(points[17:]))
		return homo

	def setInitial(self,homoPoints):
		self.initialPoints = homoPoints

	def getFundamental(self,homoPoints):
		if isinstance(self.initialPoints, list):
			raise ValueError("initialPoints has not been set or is set to []")
		else:
			mtx = cv2.findFundamentalMat(self.initialPoints,homoPoints, cv2.FM_RANSAC, 2, 0.99)
			return mtx

	def getTwoPose(self,camera,pointDetector,window):
		print("look straight into the camera and press f ")
		while(1):
			frame = camera.getNewFrame()
			window.showImage(frame)
			if cv2.waitKey(1) & 0xFF == ord('f'):
				points = pointDetector.getFacialPointsNP(frame)
				if not isinstance(points , list):
					self.setInitial(self.getHomo(points))
					break
				else:
					print("facial points not detected, please try again")
					continue
		print("look off to either side and press f")
		while(1):
			frame = camera.getNewFrame()
			window.showImage(frame)
			if cv2.waitKey(1) & 0xFF == ord('f'):
				frame2 = camera.getNewFrame()
				points = pointDetector.getFacialPointsNP(frame2)
				if not isinstance(points, list):
					pointsHomo = self.getHomo(points)
					return self.getFundamental(pointsHomo)
				else:
					print("facial points not detected, please try again")
					continue
		print("you broke it in getTwoPose")