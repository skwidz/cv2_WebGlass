import cv2
import numpy as np
from scipy import linalg

class StructureFromMotion:
	def __init__(self):
		self.initialPoints = []
		self.secondPoints = []

	def getHomo(self, points):
		homo = cv2.convertPointsToHomogeneous(np.array(points[17:]))
		return homo

	def setInitial(self,points):
		self.initialPoints = points

	def setSecond(self, points):
		self.secondPoints = points

	def getFundamental(self,homoPoints):
		if isinstance(self.initialPoints, list):
			raise ValueError("initialPoints has not been set or is set to []")
		else:
			mtx = cv2.findFundamentalMat(self.getHomo(self.initialPoints),homoPoints, cv2.FM_RANSAC, 2, 0.99)
			return mtx

	def getTwoPose(self,camera,pointDetector,window):
		print("look straight into the camera and press f ")
		while(1):
			frame = camera.getNewFrame()
			window.showImage(frame)
			if cv2.waitKey(1) & 0xFF == ord('f'):
				points = pointDetector.getFacialPointsNP(frame)
				if not isinstance(points , list):
					self.setInitial(points)
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
					retval, mask = self.getFundamental(pointsHomo)
					self.setSecond(points)
					return retval
				else:
					print("facial points not detected, please try again")
					continue

	def P1(self):
		return np.array([[1.,0.,0., 0.], [0.,1.,0.,0.],[0.,0.,1.,0.]])

	#triangulate the given poins, gives 
	def triangulate(self,Proj):
		print(Proj.dtype)
		print(self.P1().dtype)
		self.initialPoints = np.asarray(self.initialPoints, dtype=np.float64)
		self.secondPoints = np.asarray(self.secondPoints, dtype=np.float64 )
		print(self.initialPoints.dtype)
		print(self.secondPoints.dtype)
		#the max amount of points is 20, room for optimization :maybe less is better?
		#does this even work?
		# print(self.initialPoints[28:45])
		threeD = cv2.triangulatePoints(self.P1()[:3],Proj[:3],self.initialPoints[35:45].T[:2],self.secondPoints[35:45].T[:2])

		return threeD


	# def solvePnp(self):
		


#THE BELOW FUNCTIONS ARE SUBJECT TO THE FOLLOWING COPYRIGHT

# Copyright (c) 2012, Jan Erik Solem
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


	def comp_P_from_fund(self,F):
		eipole = self.compute_eipole(F.T)
		Te = self.skew(eipole)
		return np.vstack((np.dot(Te,F.T).T,eipole)).T

	def skew(self, a):
		return np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]])

	
	def compute_eipole(self, F):
		U,S,V = linalg.svd(F)
		e = V[-1]
		return e/e[2]