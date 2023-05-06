from __future__ import annotations
from typing import TYPE_CHECKING
from math import sin, cos, acos, pi

from logic.utils.vec2D import Vec2D
from logic.entity.entity import Entity
from logic.entity.entityType import EntityType
import logic.game.option as option 
import logic.utils.mathUtils as mathUtils

if TYPE_CHECKING:
    from logic.world.world import World

PLAYER_SIZE_X = 0.4
PLAYER_SIZE_Y = 0.4
PLAYER_STEP_SIZE = 0.2

DEFAULT_PLAYER_MAX_HEALTH = 100

class Player(Entity):

    def __init__(self, world:World, position:Vec2D, rotation:float):
        super().__init__(world, EntityType.PLAYER, position, rotation, Vec2D(PLAYER_SIZE_X, PLAYER_SIZE_Y), 100)


    def entity_is_in_fov(self, mob_pos, fov):
        u = (mob_pos[0] - super().get_pos()[0], mob_pos[1] - super().get_pos()[1])
        v = (cos(super().get_rotation()), sin(super().get_rotation()))
        norme_u = mathUtils.norme_2(u)
        prod_scal_uv = mathUtils.prod_scalaire_2(u, v)
        angle = acos(prod_scal_uv / norme_u)

        return angle * 180 / pi < fov // 2, angle

    def get_visibles_entity(self):
        visibles_entities = []
        world = super().get_world()
        for alien in world.get_aliens():
            if self.entity_is_in_fov(alien.get_pos(), option.OPTION.get_fov()):
                if not world.is_wall_between_entities(super().get_pos(), alien.get_pos()):
                    visibles_entities.append(alien)
        return visibles_entities