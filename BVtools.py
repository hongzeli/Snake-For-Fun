# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 12:14:01 2020

@author: lhzcom
"""

import numpy as np
import cv2

img = cv2.imread(r"C:\Users\lhzcom\Desktop\Program Park\Snake\images\head.jpg", -1)
#img = img[:221,:,:]
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
wh = np.where(img_gray > 220)
img[wh] = [0,0,0]
#img = cv2.resize(img, None, fx=100/img.shape[1], fy=100/img.shape[0], 
#                    interpolation=cv2.INTER_CUBIC)
#cv2.imwrite(r"C:\Users\lhzcom\Desktop\Program Park\Snake\images\virus_icon.png", img)
cv2.imshow("img",img)
cv2.waitKey()
























