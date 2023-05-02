from logic.utils.vec2D import Vec2D

OPTION = None

class Option:

    def __init__(self, window_dimensions:Vec2D, fov:int, view_distance:int, min_luminosity:int):
        global OPTION
        OPTION = self
        self.window_dimensions = window_dimensions
        self.fov = fov
        self.view_distance = view_distance
        self.min_luminosity = min_luminosity

    def get_window_dimensions(self) -> Vec2D:
        return self.window_dimensions

    def get_fov(self) -> int:
        return self.fov
    
    def get_view_distance(self) -> int:
        return self.view_distance

    def get_min_luminosity(self) -> float:
        return self.min_luminosity