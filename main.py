import numpy as np
import cv2 as cv
import argparse
import turtle

WIDTH, HEIGHT = 800, 600

cli = argparse.ArgumentParser()
cli.add_argument("-i", "--image", required=True,
                 help="image path")
cli.add_argument("-s", "--sigma", required=True,
                 help="median sigma percentage")
cli.add_argument("-b", "--blur", required=False,
                 help="gaussian blur intensity")
args = vars(cli.parse_args())

img = cv.imread(args["image"])
sigma = float(args["sigma"])

# noise reduction
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

if "blur" in args and args["blur"]:
    if int(args["blur"]) % 2 == 0:
        raise AssertionError(
            "gaussian blur intensity must be defined by an odd number")
    else:
        blur_intensity = (int(args["blur"]), int(args["blur"]))
        img = cv.GaussianBlur(gray, blur_intensity, 1)
else:
    img = gray

# compute the median of the single channel pixel intensities
computed_median = np.median(img)

# apply automatic Canny edge detection using the computed median
lower = int(max(0, (1.0 - sigma) * computed_median))
upper = int(min(255, (1.0 + sigma) * computed_median))
automatically_edged = cv.Canny(img, lower, upper)

# apply Canny edge detection using a wide threshold, tight
# threshold, and automatically determined threshold
wide = cv.Canny(img, 10, 200)
tight = cv.Canny(img, 225, 250)

# while True:
#     #cv.imshow("Lion_edge", np.hstack([wide, tight, automatically_edged]))

#     # black & white inversion
#     cv.imshow("Lion_edge", ~automatically_edged)
#     if cv.waitKey(1) == 27:
#         cv.destroyAllWindows()
#         break

retval, dst = cv.threshold(~automatically_edged, 127, 255, cv.THRESH_BINARY)
width = int(img.shape[1])
height = int(img.shape[0])

screen = turtle.Screen()
screen.title("monetmaker")

screen.screensize(width, height)
pen = turtle.Turtle()
pen.hideturtle()
screen.tracer(0)

for i in range(int(height/2), int(height/-2),  -1):
    pen.penup()
    pen.goto(-(width / 2), i)

    for l in range(-int(width/2), int(width/2), 1):
        pix_width = int(l + (width/2))
        pix_height = int(height/2 - i)
        if dst[pix_height, pix_width] == 0:
            pen.pendown()
            pen.forward(1)
        else:
            pen.penup()
            pen.forward(1)
    screen.update()


turtle.done()
