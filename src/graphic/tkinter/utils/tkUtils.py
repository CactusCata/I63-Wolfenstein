from logic.utils.vec2D import Vec2D

from tkinter import Tk

ONE_USE_TAG = "ONE_USE_TAG"
ONE_USE_TAG_TUPLE = (ONE_USE_TAG,)

DEFINITIVE_USE_TAG_0 = "DEFINITIVE_USE_TAG_0"
DEFINITIVE_USE_TAG_TUPLE_0 = (DEFINITIVE_USE_TAG_0,)

DEFINITIVE_USE_TAG_1 = "DEFINITIVE_USE_TAG_1"
DEFINITIVE_USE_TAG_TUPLE_1 = (DEFINITIVE_USE_TAG_1,)

DEFINITIVE_USE_TAG_2 = "DEFINITIVE_USE_TAG_2"
DEFINITIVE_USE_TAG_TUPLE_2 = (DEFINITIVE_USE_TAG_2,)

DEFINITIVE_USE_TAG_3 = "DEFINITIVE_USE_TAG_3"
DEFINITIVE_USE_TAG_TUPLE_3 = (DEFINITIVE_USE_TAG_3,)

RATIO_GUN_SIGHT_X = 0.05
RATIO_GUN_SIGHT_Y = 0.05


def place_window(root:Tk, screen_dimensions:Vec2D):
    """Place la fenetre au milieu de l'écran

    Args:
        root (Tk): Fenetre Tkinter
        screen_dimensions (Vec2D): dimensions de l'écran en pixel
    """
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    # widthxheight+x+y
    root.geometry(f"{screen_dimensions[0]}x{screen_dimensions[1]}+{(screenWidth - screen_dimensions[0]) // 2}+{(screenHeight - screen_dimensions[1]) // 2}")

def lock_window_dimensions(root:Tk, screen_dimensions:Vec2D):
    """Bloque les dimentions de la fenetre

    Args:
        root (Tk): Fenetre Tkinter
        screen_dimensions (Vec2D): dimensions de l'écran en pixel
    """
    root.minsize(screen_dimensions[0], screen_dimensions[1])
    root.maxsize(screen_dimensions[0], screen_dimensions[1])
