from typing import List
from world.blockType import BlockType
from utils.vec2D import Vec2D
from entity.player import Player
from entity.entity import Entity

WORLD_DIM_X = 16
WORLD_DIM_Y = 16

class World:

    def __init__(self, world_matrix:List[List[BlockType]]):
        self.world_matrix = world_matrix

        self.__entities = []
        self.__player = None

    def spawn_player(self, position:Vec2D, rotation:float) -> Player:
        player = Player(position=position, rotation=rotation)
        self.__player = player
        return player

    def get_player(self) -> Player:
        return self.__player