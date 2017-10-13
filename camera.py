import numpy as np
import cv2
import math


#open the webcam 
cap = cv2.VideoCapture(0)
# size = cap.shape
# print(size)
#if the webcam couldnt be opened
if not cap.isOpened(): 
	print("Could not open webcam")
	sys.exit() 

# inititalise the list of points
refpoints = []
objpoints = []
imgpoints = []

# constants for stage controll
calibration_flag = True
rendering_flag = False

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

#function to capute mouse events
def addPointClick (event, x, y, flags, params):
	#get the gobals
	global refpoints
	#capture the mouse event
	if event == cv2.EVENT_LBUTTONDOWN:
		refpoints.append((x,y))
		print(str(x) + " " + str(y))

#setup mouseclick callback
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", addPointClick)

#Capture frame by frame
ret, oldframe = cap.read()

#operations on the frame
oldgray = cv2.cvtColor(oldframe, cv2.COLOR_BGR2GRAY)
#create a mask image to draw stuff to
mask = np.zeros_like(oldframe)
# draw a circle at the center
cv2.circle(mask,(320,240), 4, (255, 0 ,0),-1)


# Calibration phase
frameCount = 0

while(1):
	frameCount+=1
	ret, frame = cap.read()
	#operations on the frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	ret, corners = cv2.findChessboardCorners(gray,(7,7), None)

	
	# draw circles on all the points
	# for i in range(len(refpoints)):
	# 	cv2.circle(mask,refpoints[i],3, (0,225,0),-1)
	img = cv2.add(frame, mask)

	#if found, add objoints, image points (after refining)
	if ret == True and frameCount%50==0:
		objpoints.append(objp)
		corners2 = cv2.cornerSubPix(gray,corners,(11,11), (-1, -1), criteria)
		imgpoints.append(corners2)
		img = cv2.drawChessboardCorners(img,(7,7), corners2, ret)
		frameCount = 0
		#img = cv2.add(frame, board)
	#display the resulting frame
	
	cv2.imshow('frame',img)
	#wait for a keypress and quit on 'q'
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#get the camera calibration matrix
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,oldgray.shape[::1], None, None )

if (ret):
	print("camera calibrated!!")
	

# while(1):

# 	#wait for a keypress and quit on 'q'
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		break
#when everything is done, release the camera
cap.release()
cv2.destroyAllWindows()