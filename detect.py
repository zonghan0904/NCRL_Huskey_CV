import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
from collections import Counter
import cv2

class Detect():
	def __init__(self):
		self.lx = []
		self.ly = []
		self.cap = cv2.VideoCapture(0)
		self.lower_red = np.array([-10,100,100])
		self.upper_red = np.array([10,255,255])
		self.lower_blue= np.array([78,158,124])
		self.upper_blue = np.array([138,255,255])

	def find_center(self):
		cx = Counter(self.lx)
		cy = Counter(self.ly)
		return (cx.most_common()[0][0], cy.most_common()[0][0])

	def find_contour(self):
		ret, self.frame = self.cap.read()
		hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
		self.mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
		self.res = cv2.bitwise_and(self.frame, self.frame, mask = self.mask)
		gray = cv2.cvtColor(self.res, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray, (11, 11), 0)
		self.binary_img = cv2.Canny(blur, 20, 160)
		self.contours = cv2.findContours(self.binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]	

	def bound_contour(self):
		for c in self.contours:
			#cv2.drawContours(frame, [c], -1, (0,255,0), 3)
			'''
			M = cv2.moments(c)
			try:
				cx = int(M["m10"]/M["m00"])
				cy = int(M["m01"]/M["m00"])
			except:
				pass
			'''		
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(self.frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
			cx = x + w / 2
			cy = y + h / 2
			if len(self.lx) >= 30:
				del self.lx[0]
				self.lx.append(cx)
			else:
				self.lx.append(cy)
			if len(self.ly) >= 30:
				del self.ly[0]
				self.ly.append(cy)
			else:
				self.ly.append(cy)
			
			(mean_x, mean_y) = self.find_center()
			cv2.circle(self.frame, (int(mean_x), int(mean_y)), 10, (1, 277, 254), -1)
			print("object's (x, y) = ({x}, {y})".format(x = mean_x, y = mean_y))	

	def show_result(self):
		cv2.imshow("frame", self.frame)
		cv2.imshow("mask", self.mask)
		cv2.imshow("canny", self.binary_img)
		cv2.imshow("res", self.res)		



if __name__ == "__main__":
	d = Detect()
	while True:
		d.find_contour()
		d.bound_contour()
		d.show_result()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break	
	d.cap.release()
	cv2.destoryAllWindows()	