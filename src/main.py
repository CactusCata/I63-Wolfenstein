from graphic.drawerManager import DrawerManager

from logic.game.option import Option
from logic.game.game import Game
from logic.utils.vec2D import Vec2D
import logic.sprite.spriteManager as spriteManager

if __name__ == "__main__":
    spriteManager.load_images()
    Option(window_dimensions=Vec2D(int(500 * 1.618), 300), fov=60)

    game = Game()
    game.get_world().spawn_player(position=Vec2D(9.5, 9.5), rotation=110)

    dm = DrawerManager()