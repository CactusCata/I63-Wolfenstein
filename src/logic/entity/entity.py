from __future__ import annotations

from typing import TYPE_CHECKING

from logic.entity.entityType import EntityType
from logic.utils.vec2D import Vec2D

if TYPE_CHECKING:
    from logic.world.world import World

from logic.world.blockType import BlockType


class Entity:
    """Classe représentant les entités du monde
    """

    def __init__(self, world: World, entity_type: EntityType, position: Vec2D, rotation: float, entity_size: Vec2D, max_health: int):
        """Constructeur

        Args:
            world (World): Monde de l'entité
            entity_type (EntityType): Type de l'entité
            position (Vec2D): Position
            rotation (float): Rotation en degré
            entity_size (Vec2D): Dimensions de l'entité
            max_health (int): Vie maximale et de départ de l'entité
        """
        self.position = position
        self.rotation = rotation
        self.world = world
        self.entity_type = entity_type
        self.entity_size = entity_size
        self.max_health = max_health
        self.health = max_health

    def can_move(self, dxy: Vec2D) -> bool:
        """Renvoie un booléan permettant de déterminer si l'entité peut se
        déplacer à l'endroit visé

        Args:
            dxy (Vec2D): delta xy

        Returns:
            bool: True si l'entité peut se déplacer. False sinon
        """

        entity_square = (
            int(self.get_pos()[0] + dxy[0] - 1/2 * self.entity_size[0]),
            int(self.get_pos()[1] + dxy[1] - 1/2 * self.entity_size[1]),
            int(self.get_pos()[0] + dxy[0] + 1/2 * self.entity_size[0]),
            int(self.get_pos()[1] + dxy[1] + 1/2 * self.entity_size[1])
        )

        if entity_square[0] != entity_square[2]:  # l'entity a passé une ligne verticale
            if dxy[0] > 0:
                rect = (entity_square[2], entity_square[1])
            elif dxy[0] < 0:
                rect = (entity_square[0], entity_square[1])

            if self.world.world_matrix[rect[1]][rect[0]] == BlockType.WALL:
                return False

        if entity_square[1] != entity_square[3]:  # l'entity a passé une ligne horizontale
            if dxy[1] > 0:
                rect = (entity_square[0], entity_square[3])
            else:
                rect = (entity_square[0], entity_square[1])

            if self.world.world_matrix[rect[1]][rect[0]] == BlockType.WALL:
                return False
            
        return True
    
    def get_entity_type(self) -> EntityType:
        """Renvoie le type l'entitée

        Returns:
            EntityType: type de l'entité
        """
        return self.entity_type

    def get_pos(self) -> Vec2D:
        """Renvoie la position actuelle du l'entity

        Returns:
            Vec2D: position de l'entité
        """
        return self.position
    
    def teleport(self, position: Vec2D) -> None:
        """Effectue une téléportation de l'entité

        Args:
            position (Vec2D): Nouvelle position de l'entité
        """
        self.position = position

    def move(self, dxy: Vec2D) -> None:
        """Effectue un déplacement relatif de l'entity

        Args:
            dxy (Vec2D): delta xy
        """
        self.position += dxy
    
    def get_rotation(self) -> float:
        """Renvoie la rotation de l'entité en degré

        Returns:
            float: Rotation de l'entité en degré
        """
        return self.rotation
    
    def set_rotatation(self, rotation: float):
        """Change la rotation de l'entité

        Args:
            rotation (float): Nouvelle rotation
        """
        self.rotation = (rotation % 360)

    def add_rotation(self, rotation: float):
        """Ajoute un delta rotation à la rotation de l'entité

        Args:
            rotation (float): delta rotation
        """
        self.rotation = (self.rotation + rotation) % 360

    def get_max_health(self) -> int:
        """Renvoie la vie maximale de l'entité

        Returns:
            int: Vie maximale de l'entité
        """
        return self.max_health
    
    def get_health(self) -> int:
        """Renvoie la vie courante de l'entité

        Returns:
            int: Vie courante de l'entité
        """
        return self.health

    def set_health(self, health:int):
        """Met à jour la vie de l'entité

        Args:
            health (int): Nouvelle vie de l'entité
        """
        self.health = health
    
    def heal(self, amount: int) -> None:
        """Soigne l'entité d'un nombre de point de vie

        Args:
            amount (int): Quantité de points de vie restaurés
        """
        self.health = min(self.health + amount, self.max_health)

    def get_world(self) -> World:
        """Renvoie le monde dans lequel se trouve l'entité

        Returns:
            World: Monde de l'entité
        """
        return self.world

    def add_damage(self, damage:int):
        """Applique une quantité de dégat sur l'entité

        Args:
            damage (int): _description_
        """
        self.set_health(max(0, self.get_health() - damage))

    @property
    def x(self) -> float:
        return self.position[0]

    @property
    def y(self) -> float:
        return self.position[1]
