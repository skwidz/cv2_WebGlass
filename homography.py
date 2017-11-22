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
    		glasses =cv2.cvtColor(glasses, cv2.COLOR_BGR2BGRA)
    		frame =cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    		mask =cv2.cvtColor(mask, cv2.COLOR_BGR2BGRA)
    		gheight, gwidth, _ = glasses.shape
    		mask[win.yoff: win.yoff+gheight, win.xoff: win.xoff+gwidth] = glasses
    		mheight, mwidth, _ = mask.shape
    		g_out = cv2.warpPerspective(mask, h, (mwidth, mheight))
    		# g_out =cv2.cvtColor(g_out, cv2.COLOR_BGR2BGRA)
    		# gheight, gwidth, _ = g_out.shape
    		# alpha_g = g_out[:,:,3]/255.0
    		# alpha_g =cv2.cvtColor(alpha_g, cv2.COLOR_BGR2BGRA)
    		# alpha_f = 1.0 - alpha_g
    		# for c in range(0,3):
    		# 	frame[win.yoff: win.yoff+gheight, win.xoff: win.xoff+gwidth, c] = (alpha_g * g_out[:,:,c] + alpha_f * frame[win.yoff:win.yoff+gheight, win.xoff: win.xoff+gwidth])
    		im = cv2.add(g_out, frame)
    		return im
    	else:
    		return f

    def newHomogWarp(self, frame, points):
        if not isinstance(points, list):
            h, status = cv2.findHomography(self.initialPoints, points[17:])
            # self.decomposeH(h)
            height, width, channels = frame.shape
            im_out = cv2.warpPerspective(frame, h, (width, height))
            return im_out
        else:
            return False

    def getRT(self, points, K):
        h, _ = cv2.findHomography(self.initialPoints, points[17:])
        _, _,  r, t = cv2.decomposeHomographyMat(h, K)
        r = np.asarray(r, dtype=np.float64)
        r, jacobian = cv2.Rodrigues(r)
        t = np.asarray(t, dtype=np.float64)
        print("getrt:\nr\n",r,"\nt\n", t)
        return r, t


    def decomposeH(self, H):
    	print("decompH")
    	pose = np.eye(3,4)
    	norm1 = float(np.linalg.norm(H[:,0]))
    	norm2 = float(np.linalg.norm(H[:,1]))
    	tnorm = float(norm2 + norm1)/ float(2.0)

    	p1 = H[:,1]
    	p2 = pose[:,1]
    	print(p1,p2 )
    	cv2.normalize(p1, p2)
    	print(p2,pose)

    
    def draw_pose(self, frame, points):
        # impoints = np.int32(impoints).reshape(-1,2)
        cv2.drawContours(img, [imgpts[:4]], -1, (200, 150, 10), -3)