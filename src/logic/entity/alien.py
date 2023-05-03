from __future__ import annotations
from typing import TYPE_CHECKING

from logic.utils.vec2D import Vec2D
from logic.entity.entity import Entity
from logic.entity.entityType import EntityType

if TYPE_CHECKING:
    from logic.world.world import World

ALIEN_SIZE_X = 0.4
ALIEN_SIZE_Y = 0.4
ALIEN_STEP_SIZE = 0.2

DEFAULT_ALIEN_MAX_HEALTH = 30

class Alien(Entity):

    def __init__(self, world:World, position:Vec2D, rotation:float):
        super().__init__(world, EntityType.ALIEN, position, rotation, Vec2D(ALIEN_SIZE_X, ALIEN_SIZE_Y), DEFAULT_ALIEN_MAX_HEALTH)
