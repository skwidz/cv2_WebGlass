import cv2
import numpy as np
import dlibDetector as d


class Homography:

    def __init__(self):
        self.initialPoints = []

    def setInitial(self, points):
        points = np.asarray(points, dtype=np.float64)
        self.initialPoints = points

    def getRefPoints(self, camera, pointDetector, window):
        print("look straight into the camera and press f")
        while(1):
            frame = camera.getNewFrame()
            window.showImage(frame)
            if cv2.waitKey(1) & 0xFF == ord('f'):
                points = pointDetector.getFacialPointsNP(frame)
                if not isinstance(points, list):
                    self.setInitial(points[17:])
                    break
                else:
                    print("facial points not detected, please try again")
                    continue

    def warpGlasses(self, f, points, win): 
    	if not isinstance(points, list):
    		frame = f.copy()
    		mask = np.zeros_like(frame)
    		fheight, fwidth, _ = frame.shape
    		h, _ = cv2.findHomography(self.initialPoints, points[17:])
    		glasses = cv2.imread("glasses.png", cv2.IMREAD_UNCHANGED)
    		glasses = win.overlayGlasses(glasses)
    		gheight, gwidth, _ = glasses.shape
    		mask[win.yoff: win.yoff+gheight, win.xoff: win.xoff+gwidth] = glasses
    		mheight, mwidth, _ = mask.shape
    		g_out = cv2.warpPerspective(mask, h, (mwidth, mheight))
    		im = cv2.add(g_out, frame)
    		return im
    	else:
    		return f
