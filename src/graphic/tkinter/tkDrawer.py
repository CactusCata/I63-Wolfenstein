from tkinter import Tk

from logic.utils.vec2D import Vec2D

from graphic.tkinter.game.gameDrawer import GameDrawer

class TkDrawner:

    def __init__(self, master:Tk):
        self.game_drawer = GameDrawer(master)

    def init_draw(self):
        self.game_drawer.draw()

    def redraw(self):
        self.game_drawer.redraw()

    def on_player_rot_event(self):
        self.redraw()

    def on_player_move_event(self, dxy:Vec2D):
        self.redraw()