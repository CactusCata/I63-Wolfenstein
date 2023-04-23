from utils.vec2D import Vec2D
from entity.entity import Entity

PLAYER_SIZE_X = 0.4
PLAYER_SIZE_Y = 0.4
PLAYER_STEP_SIZE = 0.2

class Player(Entity):

    def __init__(self, position:Vec2D, rotation:float):
        super().__init__(position, rotation)
