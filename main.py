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
Pmtx = sfmmodule.comp_P_from_fund(fmx)
threeD = sfmmodule.triangulate(Pmtx)
while(1):
	frame = cam.getNewFrame()
	points = dtec.getFacialPointsNP(frame)[17:]
	pointsFloat = np.asarray(points, "double")
	success, rvec, tvec = cv2.solvePnP(threeD[:3].T, pointsFloat, K,D)
	print("rvec")
	print(rvec)
	print("tvec")
	print(tvec)
	frame = dtec.showFacialPoints(frame,points)
	win.showImage(frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		win.destroy()
		break
