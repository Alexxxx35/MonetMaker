from cv2 import threshold
import numpy as np
import argparse
import turtle
from enum import Enum
import cv2 as cv


WIDTH, HEIGHT = 800, 600
window_size = []
COLOR_PALETTE = {"Forest1":  	(112, 78, 46), "Forest2": (121, 116, 46),
                 "Forest3": (194, 231, 127), "Forest4": (230, 248, 178), "Forest5": (112, 145, 118)}


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


def establish_color_levels(pixel_palette: dict) -> list:
    result = []
    thresold = 255 // len(pixel_palette)
    level_value = 0
    for i in range(len(pixel_palette)):
        level_value += thresold
        result.append(level_value)
    return result


def calculate_color_level(pixel_rgb: tuple) -> int:
    result = 0
    for i, value in enumerate(pixel_rgb):
        one_pixel_color_distance = abs(value-pixel_rgb[i])
        result += one_pixel_color_distance
    return result


def classify_pixels(matrix: list):
    thresholds = establish_color_levels(COLOR_PALETTE)
    for pixel_row in matrix:
        for rgb in pixel_row:
            color_level = calculate_color_level(rgb)
            for i, threshold in enumerate(thresholds):
                if color_level < threshold:
                    rgb = COLOR_PALETTE["Forest{}".format(i)]
                    break


screen = turtle.Screen()
screen.title("monetmaker")
screen.screensize(window_size[0], window_size[1])

pen = turtle.Turtle()
pen.ht()
screen.tracer(drawing_speed, 0)

print('Finished drawing')
turtle.done()
