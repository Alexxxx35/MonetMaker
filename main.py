import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import argparse

cli = argparse.ArgumentParser()
cli.add_argument("-i", "--image", required=True,
	help="image path")
cli.add_argument("-s", "--sigma", required=True,
	help="median sigma percentage")

args = vars(cli.parse_args())

cv.namedWindow('original_lion')


def f(x):
    pass


# cv.createTrackbar('lower', 'original_lion', 0, 255, f)
# cv.createTrackbar('upper', 'original_lion', 0, 255, f)

img = cv.imread(args["image"])
sigma = float(args["sigma"])

# noise reduction
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_blur = cv.GaussianBlur(gray, (5, 5), 1)

# compute the median of the single channel pixel intensities
computed_median = np.median(img_blur)

# apply automatic Canny edge detection using the computed median
lower = int(max(0, (1.0 - sigma) * computed_median))
upper = int(min(255, (1.0 + sigma) * computed_median))
automatically_edged = cv.Canny(img_blur, lower, upper)

# apply Canny edge detection using a wide threshold, tight
# threshold, and automatically determined threshold
wide = cv.Canny(img_blur, 10, 200)
tight = cv.Canny(img_blur, 225, 250)

while True:
    # x = cv.getTrackbarPos('lower', 'original_lion')
    # y = cv.getTrackbarPos('upper', 'original_lion')
    # edge = cv.Canny(img_blur, x, y)
    #cv.imshow('original_lion', edge)
    
    cv.imshow("Edges", np.hstack([wide, tight, automatically_edged]))
    if cv.waitKey(1) == 27:
        cv.destroyAllWindows()
        break
