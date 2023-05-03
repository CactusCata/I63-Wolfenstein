from math import sqrt

def euclidian_distance(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    return sqrt(dy*dy + dx*dx)

def prod_scalaire_2(u, v):
    return u[0] * v[0] + u[1] * v[1]

def norme_2(vec):
    return sqrt(prod_scalaire_2(vec, vec))