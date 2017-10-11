import numpy as np
import cv2

#open the webcam 
cap = cv2.VideoCapture(0)

#if the webcam couldnt be opened
if not cap.isOpened(): 
	print("Could not open webcam")
	sys.exit() 


while(True):
	#Capture frame by frame
	ret, frame = cap.read()

	#operations on the frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#display the resulting frame
	cv2.imshow('frame', gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#when everything is done, release the camera
cap.release()
cv2.destroyAllWindows()