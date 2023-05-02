from tkinter import Canvas, NW

from logic.utils.vec2D import Vec2D
import logic.game.game as game
import logic.imagetk.imageTkManager as imageTkManager
import logic.utils.color as color

from graphic.utils.tkUtils import DEFINITIVE_USE_TAG_TUPLE_2

import logic.font.fontManager as fontManager

class Profile:

    def __init__(self, canvas:Canvas, upleft_corner:Vec2D, profile_size:Vec2D):
        self.__game = game.GAME
        self.__canvas = canvas
        self.__upleft_corner = upleft_corner
        self.__profile_size = profile_size
        #self.__health_bar_id = -1

        self.__health_id_imgs = []


    def draw(self):
        self.draw_background_profile()
        self.draw_player_icon()
        #self.draw_health_bar()
        self.draw_health_points()

    def redraw(self):
        pass

    def draw_background_profile(self):
        self.__canvas.create_image(self.__upleft_corner[0],
                                   self.__upleft_corner[1],
                                   anchor=NW,
                                   image=imageTkManager.PROFILE_IMG_TK,
                                   tags=DEFINITIVE_USE_TAG_TUPLE_2)
        
    def draw_player_icon(self):
        self.__canvas.create_image(self.__upleft_corner[0] + 5, 
                          self.__upleft_corner[0] + 5,
                          anchor=NW,
                          image=imageTkManager.NGUYEN_SAVIOR_IMG_TK,
                          tags=DEFINITIVE_USE_TAG_TUPLE_2)
    """
    def draw_health_bar(self):
        start_x = self.__upleft_corner[0] + 10
        end_x = self.__upleft_corner[0] + 90
        start_y = self.__upleft_corner[1] + 80
        end_y = self.__upleft_corner[1] + 100
        self.__canvas.create_rectangle(start_x,
                                       start_y,
                                       end_x,
                                       end_y,
                                       fill="gray",
                                       tags=DEFINITIVE_USE_TAG_TUPLE_2)
        
        player = game.GAME.get_world().get_player()
        health_bar_color = color.health_to_color((player.get_health() * 50) / player.get_max_health())
        self.__health_bar_id = self.__canvas.create_rectangle(start_x + 2,
                                       start_y + 2,
                                       end_x - 2,
                                       end_y - 2,
                                       fill=health_bar_color,
                                       tags=DEFINITIVE_USE_TAG_TUPLE_2)
    """
        
    def draw_health_points(self):
        player = game.GAME.get_world().get_player()
        player_health = player.get_health()

        fontManager.write_text(self.__canvas, 
                               str(player_health), 
                               self.__upleft_corner + Vec2D(10, 10),
                               3)
        


        
    def on_player_get_hit(self):
        player = game.GAME.get_world().get_player()
        health_bar_color = color.health_to_color(player.get_health() * 100 / player.get_max_health())


        #self.__canvas.itemconfig(self.__health_bar_id, fill=health_bar_color)

   