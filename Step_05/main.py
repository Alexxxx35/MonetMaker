import argparse
from enum import Enum
import cv2 as cv

from classification import classify_pixels
from clustering import cluster_pixels
from draw import draw,drawKDTree,getPixelCoordinatesBygroup , drawBasic
import turtle



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


class algorithm(Enum):
    clustering = 'clustering'
    classification = 'classification'
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
cli.add_argument("-a", "--algorithm", required=False,
                 help="clustering or classification")

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


if "algorithm" in args and args["algorithm"] == "classification":
    new_matrix = classify_pixels(img, COLOR_PALETTE)
    draw(new_matrix, window_size, drawing_speed)
else:
    x, y, data_size = img.shape
    new_matrix = cluster_pixels(img)
    draw(new_matrix, window_size, drawing_speed)
    '''kmeans = cluster_pixels(img)
    mapping = kmeans.labels_.reshape((x,y))
    ngroup = len(kmeans.cluster_centers_)
    screen = turtle.Screen()
    screen.title("monetmaker")
    screen.screensize(window_size[0], window_size[1])
    pen = turtle.Turtle()
    pen.ht()
    screen.colormode(255)
    screen.tracer(drawing_speed, 0)

    for i in range(0,ngroup):
        color = kmeans.cluster_centers_[i]
        colorInt=((int(color[0]),int(color[1]),int(color[2])))
        coords = getPixelCoordinatesBygroup(mapping,i)
        pen.color(colorInt)
        drawBasic(pen,coords,img.shape,colorInt)'''

    







#draw(new_matrix, window_size, drawing_speed)

print('Finished drawing')
