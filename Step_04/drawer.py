import cv2 as cv
from scipy.spatial import KDTree
import math
import numpy as np

def get_colors_coords(image, color=0):
    coords = []
    height = len(image)
    for y, line in enumerate(image):
        for x, value in enumerate(line):
            if value == color:
                coords.append([x, height - y])
    return coords


def draw(pen, coords, shape):
    width = int(shape[1])
    height = int(shape[0])

    pen.penup()
    current_i = 0
    for i in range (0, len(coords)):
        tree = KDTree(coords, 1)

        current = coords[current_i]
        x = coords[current_i][0]
        y = coords[current_i][1]
        pen.goto(x - (width/2), y - (height/2))

        distance, indexes = tree.query([coords[current_i]], 2) # maybe add distance
        neighbour_i = indexes[0][1]
        neighbour = coords[neighbour_i]

        distance = math.dist([x, y], [neighbour[0],  neighbour[1]])
        if (distance <= 1.):
          pen.pendown()
          pen.goto(neighbour[0] - (width/2), neighbour[1]- (height/2))
          pen.penup()

        coords[current_i] = [0, 0]
        current_i = neighbour_i
