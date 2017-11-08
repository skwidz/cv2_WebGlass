#!/usr/bin/env python
import cv2
import numpy as np
import cameraController as cc
import window as w
import dlibDetector as dd
import sfm

cam = cc.CameraController()
K, D, R, T = cam.getCameraParams()
dtec = dd.DlibDetector()
win = w.Window()

while(1):
	frame = cam.getNewFrame()
	points = dtec.getFacialPointsNP(frame)
	frame = dtec.showFacialPoints(frame,points)
	win.showImage(frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		win.destroy()
		
		break
