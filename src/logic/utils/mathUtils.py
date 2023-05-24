from math import sqrt

from logic.utils.vec2D import Vec2D

def euclidian_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Renvoie la distance euclidienne entre (x1,y1) et (x2,y2)

    Args:
        x1 (float):  
        y1 (float):  
        x2 (float):  
        y2 (float):  

    Returns:
        float: distance euclidienne entre (x1,y1) et (x2,y2)
    """
    dy = y2 - y1
    dx = x2 - x1
    return sqrt(dy*dy + dx*dx)

def prod_scalaire_2(u:Vec2D, v:Vec2D) -> float:
    """Renvoie le produit scalaire de deux vecteurs à 2 dimensions

    Args:
        u (Vec2D): vecteur à 2 dimensions
        v (Vec2D): vecteur à 2 dimensions

    Returns:
        float: produit scalaire
    """
    return u[0] * v[0] + u[1] * v[1]

def norme_2(vec:Vec2D) -> float:
    """Renvoie la norme d'un vecteur

    Args:
        vec (Vec2D): vecteur

    Returns:
        float: norme du vecteur
    """
    return sqrt(prod_scalaire_2(vec, vec))