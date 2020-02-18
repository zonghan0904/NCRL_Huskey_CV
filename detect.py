import rospy
from geometry_msgs.msg import Point
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
import cv2
import time

class Detect():
	def __init__(self):
		#################### node initialization & create topic ####################
		rospy.init_node("object_detector", anonymous=False)
		self.pub = rospy.Publisher("camera_coordinate", Point, queue_size= 30)
		self.data = Point()

		#################### video stream setting ####################
		self.cap = cv2.VideoCapture(0)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
		self.time1 = time.time()
		self.time2 = time.time()

		#################### bounding object configuration ####################
		self.lower_red = np.array([-10,100,100])
		self.upper_red = np.array([10,255,255])
		self.lower_blue= np.array([78,158,124])
		self.upper_blue = np.array([138,255,255])
		self.lower_green = np.array([25, 75, 85])
		self.upper_green = np.array([50, 220, 255])
		self.contour_area = 0

		#################### camera's intrinsic parameter ####################
		self.fx = 799.577872
		self.fy = 794.397569
		self.cx = 320
		self.cy = 240
		self.object_real_width = 0.06541
		self.intrinsic_matrix = np.array([[self.fx,       0, self.cx],
									      [      0, self.fy, self.cy],
									      [      0,       0,       1]])
		try :
			self.inverse_intrinsic_matrix = np.linalg.inv(self.intrinsic_matrix)
		except:
			#sys.exit("intrinsic matrix doesn't have a inverse matrix.")
			print("intrinsic matrix doesn't have a inverse matrix.")

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
		# find the biggest target object.
		for c in self.contours:
			area = cv2.contourArea(c)
			if area > self.contour_area:
				self.contour_area = area
				contour = c

		# if target is found by camera, draw the position information on frame.
		if len(self.contours) > 0: 
			(x, y, self.w, self.h) = cv2.boundingRect(contour)
			cv2.rectangle(self.frame, (x,y), (x+self.w, y+self.h), (0, 255, 0), 2)
			self.x = x + self.w / 2
			self.y = y + self.h / 2
			cv2.circle(self.frame, (int(self.x), int(self.y)), 10, (1, 277, 254), -1)
			#print("object's (x, y) in pixel = ({x}, {y})".format(x = self.x, y = self.y))	

		# zero the contour_area
		self.contour_area = 0

	def show_result(self):
		cv2.imshow("frame", self.frame)
		#cv2.imshow("mask", self.mask)
		#cv2.imshow("canny", self.binary_img)
		#cv2.imshow("res", self.res)	

	def check_object(self):
		# check whether the target is found.
		if len(self.contours) > 0:
			return True
		else:
			return False

	def get_video_size(self):
		width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
		print("width is %d, height is %d"%(width, height))

	def object_camera_coordinate(self):
		# calculate the camera coordinate by triangle similarity theorem
		camera_coordinate_z = (self.fx / self.w) * self.object_real_width
		camera_coordinate_x = (self.x - self.cx) * camera_coordinate_z / self.fx
		camera_coordinate_y = (self.y - self.cy) * camera_coordinate_z / self.fy

		# record position information
		data = Point()
		data.x = camera_coordinate_x
		data.y = camera_coordinate_y
		data.z = camera_coordinate_z
		return data

	def object_detect(self):
		self.find_contour()
		self.bound_contour()
		self.show_result()

	def coordinate_publisher(self):
		self.data = self.object_camera_coordinate()
		self.pub.publish(self.data)

	def FPS_estimator(self):
		self.time1 = self.time2
		self.time2 = time.time()
		duration = self.time2 - self.time1
		print("FPS : %d" %(1 / duration))

	def end(self):
		self.cap.release()

if __name__ == "__main__":
	d = Detect()
	while not rospy.is_shutdown():
		d.object_detect()
		if d.check_object():
			d.coordinate_publisher()
		#d.get_video_size()
		#d.FPS_estimator()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break	
	d.end()
	cv2.destroyAllWindows()	