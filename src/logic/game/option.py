from logic.utils.vec2D import Vec2D
import json

OPTION = None

class Option:

    def __init__(self, window_dimensions:Vec2D, ratio_drawer:float, fov:int, view_distance:int, min_luminosity:int):
        global OPTION
        OPTION = self
        self.window_dimensions = window_dimensions
        self.drawer_dimensions = Vec2D(int(window_dimensions[0] * ratio_drawer), window_dimensions[1])
        self.infos_dimensions = Vec2D(int(window_dimensions[0] * (1 - ratio_drawer)), window_dimensions[1])
        self.fov = fov
        self.view_distance = view_distance
        self.min_luminosity = min_luminosity

    def get_window_dimensions(self) -> Vec2D:
        return self.window_dimensions

    def get_drawer_dimensions(self) -> Vec2D:
        return self.drawer_dimensions
    
    def get_info_dimensions(self) -> Vec2D:
        return self.infos_dimensions

    def get_fov(self) -> int:
        return self.fov
    
    def get_view_distance(self) -> int:
        return self.view_distance

    def get_min_luminosity(self) -> float:
        return self.min_luminosity
    
    def __str__(self):
        return json.dumps({
           "window_dimensions": str(self.get_window_dimensions()),
             "drawer_dimensions": str(self.get_drawer_dimensions()),
             "info_dimensions": str(self.get_info_dimensions()),
             "fov": self.get_fov(),
             "view_distance": self.get_view_distance(),
             "min_luminosity": self.get_min_luminosity()
        }, indent=4)