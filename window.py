import cv2
import numpy as np
import random


class Window:

	def __init__(self):
		self.windowName = str(random.random())
		cv2.namedWindow(self.windowName)

	def showImage(self, image):
			cv2.imshow(self.windowName, image)

	def destroy(self):
		cv2.destroyWindow(self.windowName)

	