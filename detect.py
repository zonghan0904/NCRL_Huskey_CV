import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
from collections import Counter
import cv2

def object_center(lx, ly):
	cx = Counter(lx)
	cy = Counter(ly)
	return (cx.most_common()[0][0], cy.most_common()[0][0])

cap = cv2.VideoCapture(0)
lx = []
ly = []

#lower_red = np.array([-10,100,100])
#upper_red = np.array([10,255,255])
#lower_blue= np.array([78,158,124])
#upper_blue = np.array([138,255,255])

while(True):
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower = np.array([78,158,124])
	upper = np.array([138,255,255])
	mask = cv2.inRange(hsv, lower, upper)
	res = cv2.bitwise_and(frame, frame, mask = mask)

	gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (11, 11), 0)
	binary_img = cv2.Canny(blur, 20, 160)

	contours = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	for c in contours:
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
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
		cx = x + w / 2
		cy = y + h / 2
		if len(lx) >= 30:
			del lx[0]
			lx.append(cx)
		else:
			lx.append(cy)
		if len(ly) >= 30:
			del ly[0]
			ly.append(cy)
		else:
			ly.append(cy)
		
		(mean_x, mean_y) = object_center(lx, ly)
		cv2.circle(frame, (int(mean_x), int(mean_y)), 10, (1, 277, 254), -1)
		print("object's (x, y) = ({x}, {y})".format(x = mean_x, y = mean_y))

	cv2.imshow("frame", frame)
	cv2.imshow("mask", mask)
	cv2.imshow("canny", binary_img)
	cv2.imshow("res", res)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destoryAllWindows()
