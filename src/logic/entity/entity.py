from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from math import sin, cos, pi


from logic.utils.vec2D import Vec2D

if TYPE_CHECKING:
    from logic.world.world import World

from logic.world.blockType import BlockType



class Entity:

    def __init__(self, world:World, position:Vec2D, rotation:float, entity_size:Vec2D):
        self.position = position
        self.rotation = rotation
        self.world = world
        self.entity_size = entity_size

    def can_move(self, dxy:Vec2D) -> bool:

        player_square = (
            int(self.get_pos()[0] + dxy[0] - 1/2 * self.entity_size[0]),
            int(self.get_pos()[1] + dxy[1] - 1/2 * self.entity_size[1]),
            int(self.get_pos()[0] + dxy[0] + 1/2 * self.entity_size[0]),
            int(self.get_pos()[1] + dxy[1] + 1/2 * self.entity_size[1])
        )

        
        if player_square[0] != player_square[2]: # Le joueur a passé une ligne verticale
            if dxy[0] > 0:
                rect = (player_square[2], player_square[1])
            elif dxy[0] < 0:
                rect = (player_square[0], player_square[1])
            if self.world.world_matrix[rect[1]][rect[0]] == BlockType.WALL:
                return False
            
            
        if player_square[1] != player_square[3]: # Le joueur a passé une ligne horizontale
            if dxy[1] > 0:
                rect = (player_square[0], player_square[3])
            else:
                rect = (player_square[0], player_square[1])

            if self.world.world_matrix[rect[1]][rect[0]] == BlockType.WALL:
                return False
            
        return True
        

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