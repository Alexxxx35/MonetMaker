import numpy as np
import cv2 as cv
import argparse
from enum import Enum

class blur(Enum):
    linear= 'linear'
    gaussian = 'gaussian'
    radial = 'radial'
    median = 'median'
    bilateral = 'bilateral'
    def str(self):
        return self.value


cli = argparse.ArgumentParser()
cli.add_argument("-i", "--image", required=True,
                 help="image path")

cli.add_argument("-b","--blur", type=blur, choices=list(blur), required=False,
    help="Blur method pre-applied before Canny Edge Detection (linear, gaussian or radial)")

cli.add_argument("-k","--kernel", required=False,
    help="Blur method pre-applied before Canny Edge Detection (linear, gaussian or radial)")

args = vars(cli.parse_args())

img = cv.imread(args["image"])

# noise reduction
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#Apply Blur method
if "blur" in args:
    if args["blur"] == "linear":
        blurred = cv.boxFilter(gray,-1,int(args["kernel"]),normalize=False,) if args["kernel"] else cv.boxFilter(gray,-1,3,normalize=False)

    elif args["blur"] == "gaussian":
        blurred = cv.GaussianBlur(gray,int(args["kernel"]),0) if args["kernel"] else cv.GaussianBlur(gray,3,0)

    elif args["blur"] == "median":
        blurred = cv.medianBlur(gray,int(args["kernel"])) if args["kernel"] else cv.medianBlur(gray,3)
    elif args["blur"] == "bilateral":
        blurred = cv.bilateralFilter(gray,int(args["kernel"]),75,75) if args["kernel"] else cv.medianBlur(gray,9,75,75)
    else:
        a=1






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

while True:
    cv.imshow("Canny Edge Detection", np.hstack([tight,wide,automatically_edged]))

    # black & white inversion
    #cv.imshow("Lion_edge", ~automatically_edged)
    if cv.waitKey(1) == 27:
        cv.destroyAllWindows()
        break


