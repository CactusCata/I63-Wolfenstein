from __future__ import annotations

from math import sin, cos, acos, pi, atan2, radians, degrees
from typing import TYPE_CHECKING

import logic.game.option as option
import logic.utils.mathUtils as mathUtils
from logic.entity.entity import Entity
from logic.entity.entityType import EntityType
from logic.utils.vec2D import Vec2D

if TYPE_CHECKING:
    from logic.world.world import World

PLAYER_SIZE_X = 0.4
PLAYER_SIZE_Y = 0.4
PLAYER_STEP_SIZE = 0.2
PLAYER_DAMAGE = 10

DEFAULT_PLAYER_MAX_HEALTH = 100


class Player(Entity):
    """Classe du joueur

    Args:
        Entity (_type_): Hérite de la classe Entité
    """
    def __init__(self, world: World, position: Vec2D, rotation: float):
        """Constructeur

        Args:
            world (World): Monde du joueur
            position (Vec2D): position du joueur
            rotation (float): rotation du joueur en degree
        """
        super().__init__(world, EntityType.PLAYER, position, rotation, Vec2D(PLAYER_SIZE_X, PLAYER_SIZE_Y), 100)
        self.alien_aimed = None
        self.score = 0
        self.ammo = 20

    """
    def entity_is_in_fov(self, mob_pos, fov):
        player_rotation = radians(super().get_rotation())
        u = (mob_pos[0] - super().get_pos()[0], mob_pos[1] - super().get_pos()[1])
        v = (cos(player_rotation), sin(player_rotation))
        angle = atan2(u[1], u[0]) - player_rotation
        angle = (angle + pi) % (2 * pi) - pi  # Ramener l'angle entre -pi et pi

        return abs(degrees(angle)) < fov // 2
    """

    def get_angle(self, mob_pos:Vec2D) -> float:
        """Renvoie l'angle entre le joueur et un monstre du monde

        Args:
            mob_pos (Vec2D): Position d'un monstre du monde

        Returns:
            float: angle entre le joueur et un monstre du monde
        """
        player_rotation = radians(super().get_rotation())
        u = (mob_pos[0] - super().get_pos()[0], mob_pos[1] - super().get_pos()[1])
        v = (cos(player_rotation), sin(player_rotation))
        angle = atan2(u[1], u[0]) - player_rotation
        angle = (angle + pi) % (2 * pi) - pi  # Ramener l'angle entre -pi et pi
        return degrees(angle)

    def get_visibles_entity(self) -> List[Entity]:
        """Renvoie la liste de toutes les entités visibles.
        Pour cela:
            - le monstre doit être dans le champs de vision du joueur
            - il ne doit pas y avoir de mur entre le joueur et le monstre

        Returns:
            List[Entity]: Liste des entités visibles pour le joueur
        """
        fov = option.OPTION.get_fov()
        visibles_entities = []
        world = super().get_world()
        for alien in world.get_aliens():
            alpha = self.get_angle(alien.get_pos())
            if abs(alpha) < fov // 2:
                if not world.is_wall_between_entities(super().get_pos(), alien.get_pos()):
                    visibles_entities.append((alien, alpha))

        return visibles_entities

    def increase_score(self):
        """Augmente le score du joueur de 5
        """
        self.score += 5

    def get_score(self) -> int:
        """Renvoie le score du joueur

        Returns:
            int: Score du joueur
        """
        return self.score

    def set_alien_aimed(self, alien:Alien):
        """Informe qu'un alien est dans le viseur du joueur

        Args:
            alien (Alien): alien dans la ligne de tir
        """
        self.alien_aimed = alien

    def reset_alien_aimed(self):
        """Supprime un alien de la ligne de tir
        """
        self.alien_aimed = None

    def get_alien_aimed(self) -> Alien:
        """Renvoie l'alien dans la ligne de tir.
        Peut valoir None si il n'y a pas d'alien dans
        la ligne de tir

        Returns:
            Alien: Alien dans la ligne de tir
        """
        return self.alien_aimed

    def can_shoot(self) -> bool:
        """Le joueur peut tirer ssi son nombre
        de munition est supérieur à 0.

        Returns:
            bool: Renvoie True si le nombre de munition du
            joueur est supérieur à 0. Renvoie Faux sinon
        """
        return self.ammo > 0

    def use_ammo(self):
        """Utilise une munition
        """
        if self.ammo > 0:
            self.ammo -= 1

    def get_ammo(self) -> int:
        """Renvoie le nombre de munition du joueur

        Returns:
            int: Nombre de munition du joueur
        """
        return self.ammo

    def add_ammo(self, amount: int):
        """Ajoute un nombre de munition au joueur

        Args:
            amount (int): Nombre de munition à ajouter au joueur
        """
        self.ammo += amount