from logic.sprite.sprite import Sprite

FONT_IMG = None
ALIEN_IMAGE = None

def load_images():
    """
    Charge toutes les images qui seront utilisés pour le raycastring
    """
    global FONT_IMG, ALIEN_IMAGE

    FONT_IMG = Sprite("../res/img/img.png")
    ALIEN_IMAGE = Sprite("../res/img/alien.png")