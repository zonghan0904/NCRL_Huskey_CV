import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

while 1:
    cv2.imshow("img1", frame)
    if (cv2.waitKey(1) & 0xFF == ord('y')):
        cv2.imwrite("images/pic1.png", frame)
        cv2.destroyAllWindows()
        break

cap.release()