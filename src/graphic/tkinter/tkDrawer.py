from tkinter import Tk

from logic.utils.vec2D import Vec2D

from graphic.tkinter.game.gameDrawer import GameDrawer
from graphic.tkinter.game.infoDrawer import InfoDrawer

class TkDrawner:

    def __init__(self, master:Tk):
        self.game_drawer = GameDrawer(master)
        self.info_drawer = InfoDrawer(master)

    def init_draw(self):
        self.game_drawer.draw()
        self.info_drawer.draw()

    def redraw(self):
        self.game_drawer.redraw()

    def on_player_rot_event(self):
        self.info_drawer.on_player_rot_event()
        self.redraw()

    def on_player_move_event(self, dxy:Vec2D):
        self.info_drawer.on_player_move_event(dxy)
        self.redraw()