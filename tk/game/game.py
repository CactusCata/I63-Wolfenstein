import world.worldFile as worldFile
from world.world import World

class Game:

    def __init__(self):
        self.world = worldFile.load_world_file("../res/worlds/world.dat")

    def get_world(self) -> World:
        return self.world
