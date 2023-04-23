from math import sqrt

class Vec2D:

    def __init__(self, x:int, y:int):
        self.vect = [x, y]

    def __getitem__(self, index:int):
        return self.vect[index]

    def __setitem__(self, index:int, value:int):
        self.vect[index] = value

    def __add__(self, other) -> None:
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
        return sqrt((other[0] - self.vect[0])**2 + (other[1] - self.vect[1])**2)