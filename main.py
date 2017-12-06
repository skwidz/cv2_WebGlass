#!/usr/bin/env python
import cv2
import numpy as np
import cameraController as cc
import window as w
import dlibDetector as dd
import homography as h
import glasses as glass

cam = cc.CameraController()
K, D, R, T = cam.getCameraParams()
dtec = dd.DlibDetector()
win = w.Window()
hom = h.Homography()
frame = cam.getNewFrame()
hom.getRefPoints(cam, dtec, win)
g = glass.Glasses()
g.placeGlasses(cam, win)
print("Press j to change frames, press q+w to quit")
while(1):
    frame = cam.getNewFrame()
    imagepath = g.imagePath
    points = []
    points = dtec.getFacialPointsNP(frame)
    warp = hom.warpGlasses(frame, points, win, g)
    win.showImage(warp)
    if cv2.waitKey(1) & 0xFF == ord('j'):
        g.nextFrame()
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        win.destroy()
        break
