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
	if not isinstance(points, list):
		# should use ransac
		success, rvec, tvec = cv2.solvePnP(threeD[:3].T, pointsFloat, K,D)
		(noseendPoint2D, jacobian) = cv2.projectPoints(np.array([(0.0,0.0,10.0)]), rvec, tvec, K,D)
		p1 = (points[13][0].astype(np.int32), points[13][1].astype(np.int32))
		p2 = (noseendPoint2D[0][0][0].astype(np.int32), noseendPoint2D[0][0][1].astype(np.int32))
		cv2.line(frame,p1,p2,(255,0,0),2)
	print("rvec")
	print(rvec)
	print("tvec")
	print(tvec)
	frame = dtec.showFacialPoints(frame,points)
	win.showImage(frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		win.destroy()
		break
