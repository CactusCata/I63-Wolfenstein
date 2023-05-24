from logic.utils.vec2D import Vec2D
import json

OPTION = None

class Option:
    """Permet de configurer aisement les options de l'application
    """

    def __init__(self, window_dimensions:Vec2D, ratio_drawer:float, fov:int, view_distance:int, min_luminosity:int):
        """Constructeur

        Args:
            window_dimensions (Vec2D): dimensions de la fenetre Tkinter en pixel
            ratio_drawer (float): part en pixel de largeur des zones de dessin (Tkinter et OpenGL)
            fov (int): angle du champs de vision du joueur
            view_distance (int): distance de vue des joueurs (assombrissement) 
            min_luminosity (int): luminosité minimale
        """
        global OPTION
        OPTION = self
        self.window_dimensions = window_dimensions
        self.drawer_dimensions = Vec2D(int(window_dimensions[0] * ratio_drawer), window_dimensions[1])
        self.infos_dimensions = Vec2D(int(window_dimensions[0] * (1 - ratio_drawer)), window_dimensions[1] * 2)
        self.fov = fov
        self.view_distance = view_distance
        self.min_luminosity = min_luminosity

    def get_window_dimensions(self) -> Vec2D:
        """

        Returns:
            Vec2D: Renvoie les dimensions de la fenetre Tkinter en pixel
        """
        return self.window_dimensions

    def get_drawer_dimensions(self) -> Vec2D:
        """

        Returns:
            Vec2D: Renvoie les dimensions des zones de dessin en pixel
        """
        return self.drawer_dimensions
    
    def get_info_dimensions(self) -> Vec2D:
        """

        Returns:
            Vec2D: Renvoie les dimensions des zones d'information en pixel
        """
        return self.infos_dimensions

    def get_fov(self) -> int:
        """

        Returns:
            int: Renvoie l'angle en degré du champs du vision du joueur
        """
        return self.fov
    
    def get_view_distance(self) -> int:
        """

        Returns:
            int: Renvoie la distance de vue du joueur (joue sur la luminosité)
        """
        return self.view_distance

    def get_min_luminosity(self) -> float:
        """

        Returns:
            float: Renvoie la valeur minimale de luminosité
        """
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