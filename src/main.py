from graphic.drawerManager import DrawerManager

from logic.game.option import Option
from logic.game.game import Game
from logic.utils.vec2D import Vec2D

if __name__ == "__main__":

    Option(window_dimensions=Vec2D(int(500 * 1.618), 300), fov=60)

    game = Game()
    game.get_world().spawn_player(position=Vec2D(9.5, 9.5), rotation=110)

    dm = DrawerManager()

    #game_frame = GameFrame()
    #game_frame.enable_minimap(Vec2D(600, 10), Vec2D(600 + 200, 10 + 200))
    #game_frame.run()