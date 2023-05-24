from graphic.drawerManager import DrawerManager

from logic.game.option import Option
from logic.game.game import Game
from logic.utils.vec2D import Vec2D
import logic.sprite.spriteManager as spriteManager
import logic.imagetk.imageTkManager as imageTkManager
import logic.font.fontManager as fontManager

if __name__ == "__main__":
    height = 400
    ratio_drawer = 0.7

    width = int((4 * height) / (3 * ratio_drawer))

    options = Option(window_dimensions=Vec2D(width, height), ratio_drawer=ratio_drawer, fov=60, view_distance=10, min_luminosity=0.01)
    print(f"Options: {options}")

    ratio = options.drawer_dimensions.x / options.drawer_dimensions.y
    assert abs(ratio - 4/3) < 0.01

    print("Loading textures...")
    imageTkManager.load_images()
    print("Loading font...")
    fontManager.init_separators("../res/img/font_red.png")
    fontManager.load_font("../res/img/font_red.png", ratio=0.8)
    print("Loading sprites...")
    spriteManager.load_images()

    print("Create game...")
    game = Game("world")
    game.get_world().spawn_player(position=Vec2D(9.5, 9.5), rotation=180)
    game.get_world().spawn_alien(position=Vec2D(4.0, 4.0), rotation=20)
    game.get_world().spawn_alien(position=Vec2D(4.0, 8.0), rotation=0)
    game.get_world().spawn_alien(position=Vec2D(8.0, 8.0), rotation=0)

    print("Create window...")
    dm = DrawerManager()
    fontManager.load_font_tk()
    imageTkManager.load_images_tk()
    imageTkManager.load_images_np()
    dm.run()
