import logic.world.worldFile as worldFile
from logic.world.world import World

GAME = None

class Game:

    def __init__(self):
        global GAME
        GAME = self

        self.world = worldFile.load_world_file("../res/worlds/world.dat")

    def get_world(self) -> World:
        return self.world
