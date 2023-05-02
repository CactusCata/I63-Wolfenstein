from logic.sprite.sprite import Sprite

FONT_IMG = None
MOB_IMAGE = None

def load_images():
    global FONT_IMG, MOB_IMAGE

    FONT_IMG = Sprite("../res/img/img.png")
    MOB_IMAGE = Sprite("../res/img/nguyen32.png")