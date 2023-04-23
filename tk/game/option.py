from utils.vec2D import Vec2D

OPTION = None

class Option:

    def __init__(self, window_dimensions:Vec2D, fov:int):
        global OPTION
        OPTION = self
        self.window_dimensions = window_dimensions
        self.fov = fov

    def get_window_dimensions(self) -> Vec2D:
        return self.window_dimensions

    def get_fov(self) -> int:
        return self.fov
