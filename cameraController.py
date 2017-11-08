# Camera controller
import numpy as np
import cv2
import pickle
import sys
import os.path


class CameraController:

	def __init__(self):
	
		self.camera = cv2.VideoCapture(0)
		if not self.camera.isOpened():
			print('Could not open camera')
			sys.exit()
		self.mtx = None
		self.dist = None
		self.rvecs = None
		self.tvecs = None

	#Get a new frame from the camera
	def getNewFrame(self):
		
		ret, frame = self.camera.read();
		if (ret):
			return frame 


	def setCameraParams(self,mtx,dist,rvecs,tvecs):
		
 		self.mtx = mtx
 		self.dist = dist
 		self.rvecs = rvecs
 		self.tvecs = tvecs

	def saveCalibrationToFile(self,mtx,dist,rvecs,tvecs):
		with open('calibrationData.pik', 'wb') as c:
			pickle.dump([mtx,dist,rvecs, tvecs], c, -1)
			print('Calibration Data Saved to File')


	def getCalibrationFromFile(self):
		if os.path.exists('calibrationData.pik'):
			with open('calibrationData.pik', 'rb') as l:
				mtx, dist, rvecs, tvecs = pickle.load(l)
				self.setCameraParams(mtx,dist,rvecs,tvecs)
				print('Calibration file loaded')
				return True
		else:
			print('No calibration file exsists')
			return False


	#calibrate the camera
	def calibrate(self):
		print("Camera is calibrating")
		frameCount = 0 
		frame = self.getNewFrame()
		mask = np.zeros_like(frame)
		objpoints = []
		imgpoints = []

		# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
		# TODO: figure out what these lines actually do	
		objp = np.zeros((7*7,3), np.float32)
		objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

		while(1):
			#termination criteria
			criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
			frameCount+=1; 
			frame = self.getNewFrame();
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			ret, corners = cv2.findChessboardCorners(gray,(7,7),None)
			img = cv2.add(frame, mask)
			# take a reference frame every 35 frames
			if ret == True and frameCount%15==0:
				objpoints.append(objp)

				chessboardCorners = cv2.cornerSubPix(gray, corners,(11,11), (-1, -1), criteria)
				imgpoints.append(chessboardCorners)
				# img = cv2.drawChessboardCorners(img,(7,7,), chessboardCorners, ret)
				frameCount = 0
				print("impoints has: " + str(len(imgpoints)) + " items")
				
				#break when you have 20 calibration images
				if len(imgpoints) == 30:
					break
		ret, mtx, dist, rvecs, tvecs  = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::1], None, None)
		self.saveCalibrationToFile(mtx,dist,rvecs,tvecs)
		self.setCameraParams(mtx,dist,rvecs,tvecs)

	#gets the calibration parameters
	#if none are set, reads from a file, 
	#if no file exists, calibrates the camera
	def getCameraParams(self):
		ret = self.getCalibrationFromFile();
		if not ret:
			self.calibrate()
		return self.mtx, self.dist, self.rvecs, self.tvecs

	
