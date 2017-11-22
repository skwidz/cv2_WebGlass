#!/usr/bin/env python
import cv2
import numpy as np
import cameraController as cc
import window as w
import dlibDetector as dd
import homography as h

cam = cc.CameraController()
K, D, R, T = cam.getCameraParams()
dtec = dd.DlibDetector()
win = w.Window()
hom = h.Homography()
frame = cam.getNewFrame()
hom.getRefPoints(cam, dtec, win)
win.placeGlasses(cam, win)
while(1):
    frame = cam.getNewFrame()
    points = []
    points = dtec.getFacialPointsNP(frame)
    warp = hom.warpGlasses(frame, points, win)
    win.showImage(warp)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        win.destroy()
        break

