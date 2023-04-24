from utils.vec2D import Vec2D

from tkinter import Tk

ONE_USE_TAG = "ONE_USE_TAG"
ONE_USE_TAG_TUPLE = (ONE_USE_TAG,)

DEFINITIVE_USE_TAG_0 = "DEFINITIVE_USE_TAG_0"
DEFINITIVE_USE_TAG_TUPLE_0 = (DEFINITIVE_USE_TAG_0,)

DEFINITIVE_USE_TAG_1 = "DEFINITIVE_USE_TAG_1"
DEFINITIVE_USE_TAG_TUPLE_1 = (DEFINITIVE_USE_TAG_1,)

DEFINITIVE_USE_TAG_2 = "DEFINITIVE_USE_TAG_2"
DEFINITIVE_USE_TAG_TUPLE_2 = (DEFINITIVE_USE_TAG_2,)


def place_window(root:Tk, screen_dimensions:Vec2D):
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    # widthxheight+x+y
    root.geometry(f"{screen_dimensions[0]}x{screen_dimensions[1]}+{(screenWidth - screen_dimensions[0]) // 2}+{(screenHeight - screen_dimensions[1]) // 2}")

def lock_window_dimensions(root:Tk, screen_dimensions:Vec2D):
    root.minsize(screen_dimensions[0], screen_dimensions[1])
    root.maxsize(screen_dimensions[0], screen_dimensions[1])
