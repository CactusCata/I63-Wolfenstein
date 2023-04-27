from tkinter import Canvas, Tk

import logic.game.option as option
from logic.utils.vec2D import Vec2D

from graphic.tkinter.game.gameDrawer import GameDrawer
from graphic.tkinter.game.minimapFont import MinimapFont
from graphic.utils.tkUtils import DEFINITIVE_USE_TAG_0, DEFINITIVE_USE_TAG_2, ONE_USE_TAG

class TkDrawner(Canvas):

    def __init__(self, master:Tk):
        super().__init__(master=master, 
                         width=option.OPTION.get_window_dimensions()[0], 
                         height=option.OPTION.get_window_dimensions()[1])
        
        self.__game_drawer = GameDrawer(self)
        self.__minimap = None

    def init_draw(self):
        self.__game_drawer.draw()
        self.__minimap.draw()
    
    def clear_frame(self):
        """
        Supprime tous les éléments qui devront être redessinés à la prochaine itération
        """
        self.delete(ONE_USE_TAG)

    def redraw_definitive_0(self):
        """
        Dessine toutes les formes qui n'ont pas besoin d'être redessinées
        """
        self.lift(DEFINITIVE_USE_TAG_0)
    
    def redraw_definitive_2(self):
        """
        Dessine toutes les formes qui n'ont pas besoin d'être redessinées
        """
        self.lift(DEFINITIVE_USE_TAG_2)

    def redraw_rot(self):
        self.clear_frame()

        self.redraw_definitive_0()
        self.__game_drawer.redraw()
        
        self.redraw_definitive_2()
        self.__minimap.redraw()
        self.update_idletasks()

    def redraw_move(self, dxy:Vec2D):
        self.clear_frame()

        self.redraw_definitive_0()
        self.__game_drawer.redraw()

        self.redraw_definitive_2()
        self.__minimap.update_minimap_player_move(dxy)
        self.__minimap.redraw()
        self.update_idletasks()

    def enable_minimap(self, upleft_corner:Vec2D, downright_corner:Vec2D):
        self.__minimap = MinimapFont(self, upleft_corner, downright_corner)
