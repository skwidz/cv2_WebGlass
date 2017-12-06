import cv2
import numpy as np

files = ["glasses.png", "g3.png", "shades.png"]


class Glasses:

    def __init__(self):
        self.imagePath = files[0]
        self.imageindex = 0
        self.widths = [134, 140]

    def nextFrame(self):
        self.imageindex = (self.imageindex + 1) % 3
        self.imagePath = files[self.imageindex]

    def overlayGlasses(self, overlay):
        mask = np.zeros_like(overlay)
        mask = mask[:, :, 3:]
        ov = overlay[:, :, :3]
        ovmask = overlay[:, :, 3:]
        bgmask = 255 - ovmask
        ovmask = cv2.cvtColor(ovmask, cv2.COLOR_GRAY2BGR)
        bgmask = cv2.cvtColor(bgmask, cv2.COLOR_GRAY2BGR)

        maskpart = (mask * (1 / 255.0)) * (bgmask * (1 / 255.0))
        overlaypart = (ov * (1 / 255.0)) * (ovmask * (1 / 255.0))

        im = cv2.addWeighted(maskpart, 255.0, overlaypart, 255.0, 0.0)
        return im

    def placeGlasses(self, cam, win):
        frame = cam.getNewFrame()
        print("Move glasses to correct position on face and press k")
        glasses = cv2.imread("glasses.png", flags=cv2.IMREAD_UNCHANGED)
        glasses = self.overlayGlasses(glasses)
        gheight, gwidth, _ = glasses.shape

        while(1):
            win.placing = True
            mask = np.zeros_like(frame)
            mask[win.yoff + 1: win.yoff + 1 + gheight,
                 win.xoff + 1: win.xoff + 1 + gwidth] = glasses
            frame2 = cv2.add(frame, mask)
            win.showImage(frame2)
            if cv2.waitKey(1) & 0xFF == ord('f'):
                win.placing = False
                break

    def sclaleGlasses(self, image, points, pd):
        pd_imRX = (points[38][0] + points[37][0] +
                   points[40][0] + points[41][0]) / 4
        pd_imRY = (points[38][1] + points[37][1] +
                   points[40][1] + points[41][1]) / 4
        pd_imLX = (points[43][0] + points[44][0] +
                   points[46][0] + points[47][0]) / 4
        pd_imLY = (points[43][1] + points[44][1] +
                   points[46][1] + points[47][1]) / 4
        print (int(pd_imRX))
        pd_im = (pd_imRX + pd_imLX)/2
        
        imheight, imwidth, _ = image.shape
        scalefactor = (float(pd_im) / float(pd))
        newwidth = self.widths[self.imageindex]*scalefactor
        scalefactor = imwidth/newwidth
        print(pd_im, pd, imwidth, scalefactor, newwidth)
        scaledImage = cv2.resize(image, (0, 0), fx=scalefactor, fy=scalefactor)
        return scaledImage
