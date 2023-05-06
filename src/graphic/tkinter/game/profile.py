from tkinter import Canvas, NW

from logic.utils.vec2D import Vec2D
import logic.game.game as game
import logic.imagetk.imageTkManager as imageTkManager
import logic.game.option as option

import logic.font.fontManager as fontManager

class Profile:

    def __init__(self, canvas:Canvas):
        self.__game = game.GAME
        self.__canvas = canvas
        infos_dimensions = option.OPTION.get_info_dimensions()
        self.__upleft_corner = Vec2D(0, 0)
        self.__profile_size = infos_dimensions
        #self.__health_bar_id = -1

        self.__health_id_imgs = []
        self.__pos_x_id_imgs = []
        self.__pos_y_id_imgs = []
        self.__rot_id_imgs = []


    def draw(self):
        self.draw_background_profile()
        self.draw_player_icon()
        self.draw_health_points()
        self.draw_player_pos()
        self.draw_player_rot()

    def draw_background_profile(self):
        self.__canvas.create_image(self.__upleft_corner[0],
                                   self.__upleft_corner[1],
                                   anchor=NW,
                                   image=imageTkManager.PROFILE_IMG_TK)
        
    def draw_player_icon(self):
        self.__canvas.create_image(self.__upleft_corner[0] + 5, 
                          self.__upleft_corner[0] + 5,
                          anchor=NW,
                          image=imageTkManager.NGUYEN_SAVIOR_IMG_TK)
        
    def draw_health_points(self):
        player = game.GAME.get_world().get_player()
        player_health = player.get_health()

        self.__health_id_imgs = fontManager.write_text(self.__canvas, 
                               "PV: " + str(player_health), 
                               self.__upleft_corner + Vec2D(80, 10),
                               3)
        
    def draw_player_pos(self):
        player = game.GAME.get_world().get_player()
        player_pos = player.get_pos()

        self.__pos_x_id_imgs = fontManager.write_text(self.__canvas, 
                               f"X: {player_pos[0]:.2f}", 
                               self.__upleft_corner + Vec2D(80, 25),
                               3)
        self.__pos_y_id_imgs = fontManager.write_text(self.__canvas, 
                               f"Y: {player_pos[1]:.2f}", 
                               self.__upleft_corner + Vec2D(80, 40),
                               3)

    def draw_player_rot(self):
        player = game.GAME.get_world().get_player()
        player_rot = player.get_rotation()

        self.__rot_id_imgs = fontManager.write_text(self.__canvas, 
                               f"rot: {player_rot}", 
                               self.__upleft_corner + Vec2D(80, 55),
                               3)
        

    def on_player_move_event(self, dxy:Vec2D):
        for pos_id_img in self.__pos_x_id_imgs:
            self.__canvas.delete(pos_id_img)
        self.__pos_x_id_imgs.clear()
        for pos_id_img in self.__pos_y_id_imgs:
            self.__canvas.delete(pos_id_img)
        self.__pos_y_id_imgs.clear()

        self.draw_player_pos()

    def on_player_rot_event(self):
        for rot_id_img in self.__rot_id_imgs:
            self.__canvas.delete(rot_id_img)
        self.__rot_id_imgs.clear()

        self.draw_player_rot()

    def on_player_get_hit(self):
        for health_id_img in self.__health_id_imgs:
            self.__canvas.delete(health_id_img)
        self.__health_id_imgs.clear()

        self.draw_health_points()

   