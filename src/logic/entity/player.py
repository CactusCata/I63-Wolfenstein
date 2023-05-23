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

DEFAULT_PLAYER_MAX_HEALTH = 100


class Player(Entity):
    def __init__(self, world: World, position: Vec2D, rotation: float):
        super().__init__(world, EntityType.PLAYER, position, rotation, Vec2D(PLAYER_SIZE_X, PLAYER_SIZE_Y), 100)

    def entity_is_in_fov(self, mob_pos, fov):
        player_rotation = radians(super().get_rotation())
        u = (mob_pos[0] - super().get_pos()[0], mob_pos[1] - super().get_pos()[1])
        v = (cos(player_rotation), sin(player_rotation))
        angle = atan2(u[1], u[0]) - player_rotation
        angle = (angle + pi) % (2 * pi) - pi  # Ramener l'angle entre -pi et pi

        return abs(degrees(angle)) < fov // 2

    def get_visibles_entity(self):
        visibles_entities = []
        world = super().get_world()
        for alien in world.get_aliens():
            if self.entity_is_in_fov(alien.get_pos(), option.OPTION.get_fov()):
                if not world.is_wall_between_entities(super().get_pos(), alien.get_pos()):
                    visibles_entities.append(alien)
                    print("visible")

        return visibles_entities
