from __future__ import annotations
from typing import TYPE_CHECKING


from logic.utils.vec2D import Vec2D
from logic.entity.entity import Entity

if TYPE_CHECKING:
    from logic.world.world import World

PLAYER_SIZE_X = 0.4
PLAYER_SIZE_Y = 0.4
PLAYER_STEP_SIZE = 0.2

class Player(Entity):

    def __init__(self, world:World, position:Vec2D, rotation:float):
        super().__init__(world, position, rotation, Vec2D(PLAYER_SIZE_X, PLAYER_SIZE_Y))
