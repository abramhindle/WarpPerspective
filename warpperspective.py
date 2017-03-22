# Copyright (c) 2017 OpenCV, Alexander Mordvintsev, Abid Rahman K., Abram Hindle
# License Agreement
# For Open Source Computer Vision Library
# (3-clause BSD License)
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#     Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution. Neither the names of the copyright
#     holders nor the names of the contributors may be used to endorse
#     or promote products derived from this software without specific
#     prior written permission.
# 
# This software is provided by the copyright holders and contributors
# “as is” and any express or implied warranties, including, but not
# limited to, the implied warranties of merchantability and fitness
# for a particular purpose are disclaimed. In no event shall copyright
# holders or contributors be liable for any direct, indirect,
# incidental, special, exemplary, or consequential damages (including,
# but not limited to, procurement of substitute goods or services;
# loss of use, data, or profits; or business interruption) however
# caused and on any theory of liability, whether in contract, strict
# liability, or tort (including negligence or otherwise) arising in
# any way out of the use of this software, even if advised of the
# possibility of such damage.
# 
# 
# Taken from OpenCV http://docs.opencv.org/3.1.0/da/d6e/tutorial_py_geometric_transformations.html
#
#    Alexander Mordvintsev (GSoC-2013 mentor)
#    Abid Rahman K. (GSoC-2013 intern)
# and inspired from Adrian Rosebrock http://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/

import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse




class Warper(object):
    def __init__(self,points,width=229,height=229,supersample=2,interpolation=None):
        self.points = points
        self.width  = width
        self.height = height
        self.supersample = supersample
        self.pts1 = np.float32([points[0],points[1],points[3],points[2]])
        W = self.width
        H = self.height
        self.pts2 = np.float32([[0,0],[W*supersample,0],[0,H*supersample],[W*supersample,H*supersample]])
        self.M = cv2.getPerspectiveTransform(self.pts1,self.pts2)
        self.dst = None
        if (interpolation == None):
            self.interpolation = cv2.INTER_CUBIC
        else:
            self.interpolation = interpolation

    def warp(self,img,out=None):
        W = self.width
        H = self.height
        M = self.M
        supersample = self.supersample
        if self.dst is None:
            self.dst = cv2.warpPerspective(img,M,(W*supersample,H*supersample))
        else:
            self.dst[:] = cv2.warpPerspective(img,M,(W*supersample,H*supersample))
        # unnecessarily complicated
        if supersample == 1:
            if out == None:
                return self.dst
            else:
                out[:] = self.dst
                return out
        else:
            if out == None:
                return cv2.resize(self.dst, (W,H), interpolation=self.interpolation)
            else:
                out[:] = cv2.resize(self.dst, (W,H), interpolation=self.interpolation)
                return out

    def warp_demo(self,img):
        dst = self.warp(img)
        plt.subplot(121),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)),plt.title('Input')
        plt.subplot(122),plt.imshow(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)),plt.title('Output')
        plt.show()


        
class WarpCalibrator(object):
    def __init__(self,width=229,height=229,supersample=2):
        self.window_name = "image"
        self.width = width
        self.height = height
        self.supersample = 2
    def calibrate(self,img):
        bgimage = img.copy()
        points = list()
        window_name = self.window_name
        # Inspired by Adrian Rosebrock http://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
        def click_corners(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONUP:
                points.append((x, y))
                cv2.rectangle(bgimage, (x,y), (x+2,y+2), (0, 255, 0), 2)
                cv2.imshow(window_name, bgimage)

        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, click_corners)
        cv2.imshow(window_name,bgimage)

        while True:
	    cv2.imshow(window_name, bgimage)
	    key = cv2.waitKey(1) & 0xFF
	    if len(points)==4:
		break
        def nothing(e,x,y,f,p):
            None
        cv2.setMouseCallback(window_name, nothing)

        warper = Warper(points=points,width=self.width,height=self.height,supersample=self.supersample)
        return warper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Demo Calibrate images for perspective correction')
    parser.add_argument('demo', type=str, nargs=1, default="test2.jpg",
                    help='Input image to correct perspective on!')
    parser.add_argument('--width', type=int, nargs=1,default=512,
                        help='Width for Warping')
    parser.add_argument('--height', type=int, nargs=1,default=512,
                        help='height for Warping')
    args = parser.parse_args()
    img = cv2.imread(args.demo[0])
    # instantiate this, it is a builder for the warper
    wc = WarpCalibrator(width=args.width,height=args.height)
    # make a blocking GUI that calibrates and produces a warper
    warper = wc.calibrate(img)
    # warp the image
    warped = warper.warp(img)
    cv2.imshow(wc.window_name, warped)
    cv2.waitKey(0)
    warper.warp_demo(img)
