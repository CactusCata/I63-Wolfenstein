from utils.vec2D import Vec2D

class Entity:

    def __init__(self, position:Vec2D, rotation:float):
        self.position = position
        self.rotation = rotation

    def get_pos(self) -> Vec2D:
        """
        Renvoie la position actuelle du joueur
        """
        return self.position
    
    def teleport(self, position:Vec2D) -> None:
        """
        Effectue une téléportation du joueur
        """
        self.position = position

    def move(self, dxy:Vec2D) -> None:
        """
        Effectue un déplacement relatif du joueur
        """
        self.position += dxy
    
    def get_rotation(self) -> float:
        """
        Effectue une rotation du joueur
        """
        return self.rotation
    
    def set_rotatation(self, rotation:float):
        """
        Change la rotation du joueur
        """
        self.rotation = (rotation % 360)

    def add_rotation(self, rotation:float):
        self.rotation = (self.rotation + rotation) % 360