from __future__ import annotations
from typing import TYPE_CHECKING

from random import random
from math import cos, sin, pi

import logic.utils.mathUtils as mathUtils

from logic.utils.vec2D import Vec2D
from logic.entity.entity import Entity
from logic.entity.entityType import EntityType

if TYPE_CHECKING:
    from logic.world.world import World

ALIEN_SIZE_X = 0.4
ALIEN_SIZE_Y = 0.4
ALIEN_STEP_SIZE = 0.5
ALIEN_DAMAGE = 8
ALIEN_RANGE = 3
ALIEN_MOVE_FREQUENCY_MS = 500

DEFAULT_ALIEN_MAX_HEALTH = 30

class Alien(Entity):

    def __init__(self, world:World, position:Vec2D, rotation:float):
        super().__init__(world, EntityType.ALIEN, position, rotation, Vec2D(ALIEN_SIZE_X, ALIEN_SIZE_Y), DEFAULT_ALIEN_MAX_HEALTH)

    def move(self):
        """Mouvement de l'alien
        """
        random_alpha = 2 * pi * random()
        dx = cos(random_alpha) * ALIEN_STEP_SIZE
        dy = sin(random_alpha) * ALIEN_STEP_SIZE
        dxy = Vec2D(dx, dy)

        if super().can_move(dxy):
            super().move(dxy)

    def try_attack(self):
        """Tente une attaque et la réalise si elle le peut
        """
        player = super().get_world().get_player()
        player_pos = player.get_pos()

        if mathUtils.euclidian_distance(player_pos[0], player_pos[1], super().get_pos()[0], super().get_pos()[1]) <= ALIEN_RANGE:
            player.add_damage(ALIEN_DAMAGE)