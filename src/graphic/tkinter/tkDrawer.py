from tkinter import Tk

from logic.utils.vec2D import Vec2D

from graphic.tkinter.game.gameDrawer import GameDrawer

class TkDrawner:
    """Classe qui permet de manager l'affichage Tkinter
    """

    def __init__(self, master:Tk):
        self.game_drawer = GameDrawer(master)

    def init_draw(self):
        """Premier dessin
        """
        self.game_drawer.draw()

    def redraw(self):
        """Prochain dessins
        """
        self.game_drawer.redraw()

    def on_player_rot_event(self):
        """Lorsque un joueur se tourne
        """
        self.redraw()

    def on_player_move_event(self, dxy:Vec2D):
        """Lorsque un joueur se déplacer

        Args:
            dxy (Vec2D): delta dxy
        """
        self.redraw()