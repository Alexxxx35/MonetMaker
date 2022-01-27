import numpy as np
import argparse
import turtle
from enum import Enum
import cv2 as cv
from scipy.spatial import KDTree

WIDTH, HEIGHT = 800, 600
window_size = []


class blur(Enum):
    linear = 'linear'
    gaussian = 'gaussian'
    radial = 'radial'
    median = 'median'
    bilateral = 'bilateral'

    def str(self):
        return self.value


cli = argparse.ArgumentParser()
cli.add_argument("-i", "--image", required=True,
                 help="image path")

cli.add_argument("-b", "--blur", type=blur, choices=list(blur), required=False,
                 help="blur method pre-applied before Canny Edge Detection (linear, gaussian or radial)")
cli.add_argument("-k", "--kernel", required=False,
                 help="kernel level of blurring")
cli.add_argument("-W", "--width", required=False,
                 help="window width")
cli.add_argument("-H", "--height", required=False,
                 help="window height")
cli.add_argument("-s", "--speed", required=False,
                 help="drawing speed in pixels")

args = vars(cli.parse_args())

img = cv.imread(args["image"])

# noise reduction
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


# Apply Blur method
if "blur" in args:
    if args["blur"] == "linear":
        blurred = cv.boxFilter(gray, -1, int(args["kernel"]), normalize=False,
                               ) if args["kernel"] else cv.boxFilter(gray, -1, 3, normalize=False)
    elif args["blur"] == "median":
        blurred = cv.medianBlur(
            gray, int(args["kernel"])) if args["kernel"] else cv.medianBlur(gray, 3)
    elif args["blur"] == "bilateral":
        blurred = cv.bilateralFilter(gray, int(
            args["kernel"]), 75, 75) if args["kernel"] else cv.medianBlur(gray, 9, 75, 75)
    else:
        # gaussian blur by default
        blurred = cv.GaussianBlur(gray, (int(
            args["kernel"]), int(
            args["kernel"])), 0) if args["kernel"] else cv.GaussianBlur(gray, (3, 3), 0)

if "speed" in args and args["speed"]:
    drawing_speed = int(args["speed"])
else:
    drawing_speed = 0

if "width" in args and "height" in args and args["width"] and args["height"]:
    window_size = (int(args["width"]), int(args["height"]))
else:
    window_size.append(WIDTH)
    window_size.append(HEIGHT)

computed_median = np.median(gray)
# apply automatic Canny edge detection using the computed median
lower_treshold = (1.0 - 0.33) * computed_median

# Here we consider that the max value the image is 255 ( 8bit images)
upper_treshold = int(min(255, (1.0 + 0.33) * computed_median))


automatically_edged = ~cv.Canny(img, lower_treshold, upper_treshold)
wide = ~cv.Canny(img, 10, 200)
tight = ~cv.Canny(img, 225, 250)

retval, dst = cv.threshold(automatically_edged, 127, 255, cv.THRESH_BINARY)

screen = turtle.Screen()
screen.title("monetmaker")
screen.screensize(window_size[0], window_size[1])

pen = turtle.Turtle()
pen.ht()
screen.tracer(drawing_speed, 0)


def get_black_points_coordinates(matrix):
    picture_coordinates = []
    height = len(matrix)
    width = len(matrix[0])

    for y_index, line in enumerate(matrix):
        for x_index, binary_value in enumerate(line):
            if binary_value == 0:
                picture_coordinates.append(
                    (x_index-width/2, height-y_index-height/2))

    return picture_coordinates


coordinates = get_black_points_coordinates(dst)
current_index = 0
for i in range(len(coordinates)):
    tree = KDTree(coordinates, 1)
    current_point = coordinates[current_index]
    distance, indexes = tree.query([coordinates[0]], 2)  # maybe add distance
    neighbour_index = indexes[0][1]
    neighbour = coordinates[neighbour_index]
    pen.pendown()
    pen.goto(neighbour)
    pen.penup()
    coordinates[current_index] = [0, 0]
    print(neighbour)
    current_index = neighbour_index
    coordinates = [point for point in coordinates if point != [0, 0]]
