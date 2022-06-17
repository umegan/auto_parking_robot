import numpy as np
import cv2 as cv

image = cv.imread('datas/IMG_0381.jpg')
hsvimage = cv.cvtColor(image, cv.COLOR_BGR2HSV)
lower = np.array([135, 0, 0], dtype="uint8")
upper = np.array([175, 255, 255], dtype="uint8")
mask = cv.inRange(hsvimage, lower, upper)

cv.imshow("mask", mask)
cv.waitKey()