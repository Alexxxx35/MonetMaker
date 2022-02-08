import argparse
import turtle
from enum import Enum
import cv2 as cv


WIDTH, HEIGHT = 800, 800
window_size = []
COLOR_PALETTE = {0: (112, 78, 46), 1: (121, 116, 46),
                 2: (194, 231, 127), 3: (230, 248, 178),
                 4: (112, 145, 118)}


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


def pixel_closest_color_from_palette(pixel_rgb: tuple, color_palette: dict) -> tuple:
    distances = []
    result = 0
    for rgb_tuple in color_palette.values():
        for i, rgb_value in enumerate(pixel_rgb):
            pixel_color_distance = abs(rgb_value-rgb_tuple[i])
            result += pixel_color_distance
        distances.append(result)
        result = 0
    index_of_smallest_distance = distances.index(min(distances))
    return color_palette[index_of_smallest_distance]


def classify_pixels(matrix: list) -> list:
    for pixel_row in matrix:
        for i, rgb in enumerate(pixel_row):
            pixel_row[i] = pixel_closest_color_from_palette(
                rgb, COLOR_PALETTE)
    return matrix


def draw(new_matrix: list) -> None:
    screen = turtle.Screen()
    screen.title("monetmaker")
    screen.screensize(window_size[0], window_size[1])
    screen.colormode(255)
    pen = turtle.Turtle()
    # pen.ht()
    screen.tracer(drawing_speed)
    image_width = new_matrix.shape[1]
    image_height = new_matrix.shape[0]
    for y in range(int(image_height/2), int(image_height/-2),  -1):
        pen.penup()
        pen.goto(-(image_width / 2), y)
        pen.pendown()
        for x in range(-int(image_width/2), int(image_width/2), 1):
            pix_width = int(x + (image_width/2))
            pix_height = int(image_height/2 - y)
            pen.color(new_matrix[pix_height, pix_width])
            pen.forward(1)
            print(pix_width, pix_height)
    return


new_matrix = classify_pixels(img)
draw(new_matrix)
print('Finished drawing')
turtle.done()
