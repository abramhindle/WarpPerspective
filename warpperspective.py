# OpenCV http://docs.opencv.org/3.1.0/da/d6e/tutorial_py_geometric_transformations.html
#
#    Alexander Mordvintsev (GSoC-2013 mentor)
#    Abid Rahman K. (GSoC-2013 intern)
#
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread("test2.jpg")
rows,cols,ch = img.shape
 
points = []
bgimage = img.copy()
# Inspired by Adrian Rosebrock http://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
def click_and_crop(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONUP:
        points.append((x, y))
        cv2.rectangle(bgimage, (x,y), (x+2,y+2), (0, 255, 0), 2)
        cv2.imshow("image", bgimage)

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
cv2.imshow("image",bgimage)

while True:
	cv2.imshow("image", bgimage)
	key = cv2.waitKey(1) & 0xFF
	if len(points)==4:
		break

W=H=229
pts1 = np.float32([points[0],points[1],points[3],points[2]])
pts2 = np.float32([[0,0],[W,0],[0,H],[W,H]])
 
M = cv2.getPerspectiveTransform(pts1,pts2)
 
dst = cv2.warpPerspective(img,M,(W,H))
 
plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()

