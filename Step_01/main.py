import numpy as np
import cv2 as cv
import argparse

cli = argparse.ArgumentParser()
cli.add_argument("-i", "--image", required=True,
                 help="image path")


args = vars(cli.parse_args())

img = cv.imread(args["image"])

# noise reduction
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


computed_median = np.median(gray)
# apply automatic Canny edge detection using the computed median
lower_treshold = (1.0 - 0.33) * computed_median

#Here we consider that the max value the image is 255 ( 8bit images)
upper_treshold = int(min(255, (1.0 + 0.33) * computed_median))


automatically_edged = ~cv.Canny(img, lower_treshold, upper_treshold)


# apply Canny edge detection using a wide threshold, tight
# threshold, and automatically determined threshold
wide = ~cv.Canny(img, 10, 200)
tight = ~cv.Canny(img, 225, 250)

cv.imshow("Canny Edge Detection", np.hstack([tight,wide,automatically_edged]))
cv.waitKey()
cv.destroyAllWindows()
