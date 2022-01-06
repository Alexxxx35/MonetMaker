import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
cv.namedWindow('original_lion')


def f(x):
    pass


cv.createTrackbar('lower', 'original_lion', 0, 255, f)
cv.createTrackbar('upper', 'original_lion', 0, 255, f)
img = cv.imread('images/lion.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
while True:
    x = cv.getTrackbarPos('lower', 'original_lion')
    y = cv.getTrackbarPos('upper', 'original_lion')
    print(x, y)
    edge = cv.Canny(gray, x, y)

    cv.imshow('original_lion', edge)

    if cv.waitKey(1) == 27:
        cv.destroyAllWindows()
        break
