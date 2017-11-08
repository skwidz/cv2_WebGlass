#!/usr/bin/env python
import cv2
import numpy as np
import cameraController as cc
import window as w
import dlibDetector as dd
import structureFromMotion as sfm


cam = cc.CameraController()
K, D, R, T = cam.getCameraParams()
dtec = dd.DlibDetector()
win = w.Window()
sfmmodule = sfm.StructureFromMotion()

fmx = sfmmodule.getTwoPose(cam, dtec,win)
print("fund")
print(fmx)
print('P:')
Pmtx = sfmmodule.comp_P_from_fund(fmx)
print(Pmtx)
sfmmodule.triangulate(Pmtx)

#demo of the dlib tracking
while(1):
	frame = cam.getNewFrame()
	points = dtec.getFacialPointsNP(frame)
	frame = dtec.showFacialPoints(frame,points[17:])
	win.showImage(frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		win.destroy()
		break
