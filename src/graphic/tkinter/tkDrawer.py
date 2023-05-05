from tkinter import Canvas, Tk, S, NW

import logic.game.option as option
from logic.utils.vec2D import Vec2D
import logic.imagetk.imageTkManager as imageTkManager

from graphic.tkinter.game.gameDrawer import GameDrawer
from graphic.tkinter.game.minimapFont import MinimapFont
from graphic.tkinter.game.profile import Profile
from graphic.utils.tkUtils import DEFINITIVE_USE_TAG_0, DEFINITIVE_USE_TAG_2, DEFINITIVE_USE_TAG_3, ONE_USE_TAG

import random

from time import time

class TkDrawner(Canvas):

    def __init__(self, master:Tk):
        super().__init__(master=master, 
                         width=option.OPTION.get_window_dimensions()[0], 
                         height=option.OPTION.get_window_dimensions()[1])
        
        self.__game_drawer = GameDrawer(self)
        self.__minimap = None
        self.__profile = Profile(self, Vec2D(10, 10), Vec2D(110, 120))
        self.timestamp = time()
        self.frame_amount = 0

    def init_draw(self):
        self.create_ground()
        self.create_roof()
        self.__game_drawer.draw()
        self.__minimap.draw()
        self.__profile.draw()
        self.create_gun()
        self.create_gun_sight()
        #print(len(self.find("all")))

    def create_ground(self):
        self.create_image(0, 
                          option.OPTION.get_window_dimensions()[1] // 2,
                          anchor=NW,
                          image=random.choice(imageTkManager.GROUND_IMG_TK),
                          tags=ONE_USE_TAG)

    def create_roof(self):
        self.create_image(0, 
                          0,
                          anchor=NW,
                          image=random.choice(imageTkManager.ROOF_IMG_TK),
                          tags=ONE_USE_TAG)

    def create_gun(self):
        self.create_image(option.OPTION.get_window_dimensions()[0] // 2 - 6 ,
                          option.OPTION.get_window_dimensions()[1],
                          anchor=S,
                          image=imageTkManager.GUN_IMG_TK, 
                          tags=DEFINITIVE_USE_TAG_2)
        
    def create_gun_sight(self):
        self.create_line(option.OPTION.get_window_dimensions()[0] // 2 - 5,
                         option.OPTION.get_window_dimensions()[1] // 2,
                         option.OPTION.get_window_dimensions()[0] // 2 + 5,
                         option.OPTION.get_window_dimensions()[1] // 2,
                         tags=DEFINITIVE_USE_TAG_2,
                         fill="white")
        
        self.create_line(option.OPTION.get_window_dimensions()[0] // 2,
                         option.OPTION.get_window_dimensions()[1] // 2 - 5,
                         option.OPTION.get_window_dimensions()[0] // 2,
                         option.OPTION.get_window_dimensions()[1] // 2 + 5,
                         tags=DEFINITIVE_USE_TAG_2,
                         fill="white")  


    def clear_frame(self):
        """
        Supprime tous les éléments qui devront être redessinés à la prochaine itération
        """
        self.delete(ONE_USE_TAG)

    def redraw_roof(self):
        self.create_roof()

    def redraw_ground(self):
        self.create_ground()

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

    def redraw_definitive_3(self):
        self.lift(DEFINITIVE_USE_TAG_3)

    def redraw_rot(self):
        timestamp = time()
        if int(self.timestamp) != int(timestamp):
            self.timestamp = timestamp
            print(self.frame_amount)
            self.frame_amount = 0
        self.frame_amount += 1

        self.clear_frame()

        self.__profile.on_player_rotate()

        self.redraw_ground()
        self.redraw_roof()
        self.redraw_definitive_0()
        self.__game_drawer.redraw()
        
        self.redraw_definitive_2()
        self.__minimap.redraw()

        #print(len(self.find("all")))

        self.update_idletasks()

    def redraw_move(self, dxy:Vec2D):
        timestamp = time()
        if int(self.timestamp) != int(timestamp):
            self.timestamp = timestamp
            print(self.frame_amount)
            self.frame_amount = 0
        self.frame_amount += 1
        self.clear_frame()

        self.__profile.on_player_move()

        self.redraw_ground()
        self.redraw_roof()
        self.redraw_definitive_0()
        self.__game_drawer.redraw()

        self.redraw_definitive_2()
        self.__minimap.update_minimap_player_move(dxy)
        self.__minimap.redraw()


        #print(len(self.find("all")))

        self.update_idletasks()

    def enable_minimap(self, upleft_corner:Vec2D, downright_corner:Vec2D):
        self.__minimap = MinimapFont(self, upleft_corner, downright_corner)
