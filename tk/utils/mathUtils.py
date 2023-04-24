from math import sqrt, pow

def euclidian_distance(x1, y1, x2, y2):
    return sqrt(pow(y2 - y1, 2) + pow(x2 - x1, 2))