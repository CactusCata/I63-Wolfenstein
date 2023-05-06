from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from math import sin, cos, pi


from logic.utils.vec2D import Vec2D
from logic.entity.entityType import EntityType

if TYPE_CHECKING:
    from logic.world.world import World

from logic.world.blockType import BlockType

class Entity:

    def __init__(self, world:World, entity_type:EntityType, position:Vec2D, rotation:float, entity_size:Vec2D, max_health:int):
        self.position = position
        self.rotation = rotation
        self.world = world
        self.entity_type = entity_type
        self.entity_size = entity_size
        self.max_health = max_health
        self.health = max_health

    def can_move(self, dxy:Vec2D) -> bool:

        entity_square = (
            int(self.get_pos()[0] + dxy[0] - 1/2 * self.entity_size[0]),
            int(self.get_pos()[1] + dxy[1] - 1/2 * self.entity_size[1]),
            int(self.get_pos()[0] + dxy[0] + 1/2 * self.entity_size[0]),
            int(self.get_pos()[1] + dxy[1] + 1/2 * self.entity_size[1])
        )

        
        if entity_square[0] != entity_square[2]: # l'entity a passé une ligne verticale
            if dxy[0] > 0:
                rect = (entity_square[2], entity_square[1])
            elif dxy[0] < 0:
                rect = (entity_square[0], entity_square[1])
            if self.world.world_matrix[rect[1]][rect[0]] == BlockType.WALL:
                return False
            
            
        if entity_square[1] != entity_square[3]: # l'entity a passé une ligne horizontale
            if dxy[1] > 0:
                rect = (entity_square[0], entity_square[3])
            else:
                rect = (entity_square[0], entity_square[1])

            if self.world.world_matrix[rect[1]][rect[0]] == BlockType.WALL:
                return False
            
        return True
    
    def get_entity_type(self) -> EntityType:
        """
        Renvoie le type l'entitée
        """
        return self.entity_type

    def get_pos(self) -> Vec2D:
        """
        Renvoie la position actuelle du l'entity
        """
        return self.position
    
    def teleport(self, position:Vec2D) -> None:
        """
        Effectue une téléportation de l'entity
        """
        self.position = position

    def move(self, dxy:Vec2D) -> None:
        """
        Effectue un déplacement relatif de l'entity
        """
        self.position += dxy
    
    def get_rotation(self) -> float:
        """
        Effectue une rotation du l'entity
        """
        return self.rotation
    
    def set_rotatation(self, rotation:float):
        """
        Change la rotation de l'entity
        """
        self.rotation = (rotation % 360)

    def add_rotation(self, rotation:float):
        self.rotation = (self.rotation + rotation) % 360

    def get_max_health(self) -> int:
        return self.max_health
    
    def get_health(self) -> int:
        return self.health
    
    def heal(self, amount:int) -> None:
        self.health = min(self.health + amount, self.max_health)

    def get_world(self) -> World:
        return self.world