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
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
		self.lower_red = np.array([-10,100,100])
		self.upper_red = np.array([10,255,255])
		self.lower_blue= np.array([78,158,124])
		self.upper_blue = np.array([138,255,255])
		self.lower_green = np.array([25, 75, 85])
		self.upper_green = np.array([50, 220, 255])
		self.fx = 799.577872
		self.fy = 794.397569
		self.cx = 320
		self.cy = 240
		self.real_width = 0.06541
		self.area = 0
		self.intrinsic_matrix = np.array([[self.fx,       0, self.cx],
									      [      0, self.fy, self.cy],
									      [      0,       0,       1]])
		try :
			self.inverse_intrinsic_matrix = np.linalg.inv(self.intrinsic_matrix)
		except:
			sys.exit("intrinsic matrix doesn't have a inverse matrix.")

	def find_contour(self):
		ret, self.frame = self.cap.read()
		hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
		self.mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
		self.res = cv2.bitwise_and(self.frame, self.frame, mask = self.mask)
		gray = cv2.cvtColor(self.res, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray, (11, 11), 0)
		self.binary_img = cv2.Canny(blur, 20, 160)
		self.contours = cv2.findContours(self.binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]	

	def bound_contour(self):
		for c in self.contours:
			area = cv2.contourArea(c)
			if area > self.area:
				self.area = area
				self.contour = c

		if len(self.contours) > 0: 
			(x, y, self.w, self.h) = cv2.boundingRect(self.contour)
			cv2.rectangle(self.frame, (x,y), (x+self.w, y+self.h), (0, 255, 0), 2)
			self.cx = x + self.w / 2
			self.cy = y + self.h / 2
			cv2.circle(self.frame, (int(self.cx), int(self.cy)), 10, (1, 277, 254), -1)
			print("object's (x, y) in pixel = ({x}, {y})".format(x = self.cx, y = self.cy))	

		self.area = 0

	def show_result(self):
		cv2.imshow("frame", self.frame)
		#cv2.imshow("mask", self.mask)
		#cv2.imshow("canny", self.binary_img)
		cv2.imshow("res", self.res)		


	def get_video_size(self):
		width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
		print("width is %d, height is %d"%(width, height))

	def object_camera_coordinate(self):
		self.camera_coordinate_x = (self.cx - 320) / self.fx
		self.camera_coordinate_y = (self.cy - 240) / self.fy
		self.camera_coordinate_z = (self.fx / self.w) * self.real_width
		print("object's (x, y, z) in camera coordinate = ({x}, {y}, {z})".format(x = self.camera_coordinate_x,
																				 y = self.camera_coordinate_y,
																				 z = self.camera_coordinate_z))

if __name__ == "__main__":
	d = Detect()
	while True:
		d.find_contour()
		d.bound_contour()
		d.show_result()
		if len(d.contours) > 0:
			d.object_camera_coordinate()
		#d.get_video_size()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break	
	d.cap.release()
	cv2.destoryAllWindows()	