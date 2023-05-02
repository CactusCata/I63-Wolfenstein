from graphic.drawerManager import DrawerManager

from logic.game.option import Option
from logic.game.game import Game
from logic.utils.vec2D import Vec2D
import logic.sprite.spriteManager as spriteManager
import logic.imagetk.imageTkManager as imageTkManager
import logic.font.fontManager as fontManager

if __name__ == "__main__":
    Option(window_dimensions=Vec2D(int(500 * 1.618), 300), fov=60, view_distance=10, min_luminosity=0.01)
    
    print("Loading textures...")
    imageTkManager.load_images()
    print("Loading font...")
    #fontManager.init_separators("../res/img/font_red.png")
    #fontManager.load_font("../res/img/font_red.png")
    print("Loading sprites...")
    spriteManager.load_images()

    print("Create game...")
    game = Game()
    game.get_world().spawn_player(position=Vec2D(9.5, 9.5), rotation=110)
    game.get_world().spawn_alien(position=Vec2D(4.0, 4.0), rotation=20)

    print("Create window...")
    dm = DrawerManager()
    #fontManager.load_font_tk()
    imageTkManager.load_images_tk()
    dm.run()