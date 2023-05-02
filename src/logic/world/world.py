from typing import List, TYPE_CHECKING


from logic.world.blockType import BlockType
from logic.utils.vec2D import Vec2D
from logic.entity.player import Player
from logic.entity.alien import Alien

from logic.entity.entity import Entity

WORLD_DIM_X = 16
WORLD_DIM_Y = 16

class World:

    def __init__(self, world_matrix:List[List[BlockType]]):
        self.world_matrix = world_matrix

        self.__aliens = []
        self.__player = None

    def spawn_player(self, position:Vec2D, rotation:float) -> Player:
        player = Player(world=self, position=position, rotation=rotation)
        self.__player = player
        return player

    def get_player(self) -> Player:
        return self.__player
    
    def spawn_alien(self, position:Vec2D, rotation:float) -> Player:
        alien = Alien(world=self, position=position, rotation=rotation)
        self.__aliens.append(alien)

    def get_aliens(self):
        return self.__aliens