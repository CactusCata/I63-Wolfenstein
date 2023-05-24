from __future__ import annotations

from math import sqrt


class Vec2D:
    """
    Permet de manipuler des couples.
    """
    def __init__(self, x: float, y: float):
        self.vect = [x, y]

    def __getitem__(self, index: int) -> float:
        return self.vect[index]

    def __setitem__(self, index: int, value: float):
        self.vect[index] = value

    def __add__(self, other: Vec2D) -> Vec2D:
        return Vec2D(self.vect[0] + other[0], self.vect[1] + other[1])

    def __iadd__(self, other):
        self.vect[0] += other.vect[0]
        self.vect[1] += other.vect[1]

        return self

    def __sub__(self, other):
        return Vec2D(self.vect[0] - other[0], self.vect[1] - other[1])
    
    def __isub__(self, other):
        self.vect[0] -= other.vect[0]
        self.vect[1] -= other.vect[1]
        return self

    def __str__(self):
        return str(self.vect)
    
    def distance(self, other) -> float:
        dx = other[0] - self.vect[0]
        dy = other[1] - self.vect[1]

        return sqrt(dx * dx + dy * dy)

    @property
    def x(self) -> float:
        return self.vect[0]

    @property
    def y(self) -> float:
        return self.vect[1]
