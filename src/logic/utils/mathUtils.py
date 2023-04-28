from math import sqrt

def euclidian_distance(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    return sqrt(dy*dy + dx*dx)