from tkinter import Canvas, NW

from logic.utils.vec2D import Vec2D
import logic.game.game as game
import logic.imagetk.imageTkManager as imageTkManager
import logic.game.option as option

import logic.font.fontManager as fontManager

class Profile:

    """Affiche les informations du joueur
    """

    def __init__(self, canvas:Canvas):
        """Constructeur

        Args:
            canvas (Canvas): canvas qui contiendra les informations du joueur
        """
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
        self.__score_imgs = []
        self.__ammo_imgs = []

        self.__player_icon_id = -1
        self.__player_current_img = None


    def draw(self):
        """Dessine les informations du joueur
        """
        self.draw_background_profile()
        self.draw_player_icon()
        self.draw_health_points()
        self.draw_player_pos()
        self.draw_player_rot()
        self.draw_player_score()
        self.draw_player_ammo()

    def draw_background_profile(self):
        """Dessine l'image de fond du profil
        """
        self.__canvas.create_image(self.__upleft_corner[0],
                                   self.__upleft_corner[1],
                                   anchor=NW,
                                   image=imageTkManager.PROFILE_IMG_TK)
        
    def draw_player_icon(self):
        """Dessine l'image Nguyen, notre gouroux
        """
        player = game.GAME.get_world().get_player()
        player_health_percent = player.get_health() / player.get_max_health()
        img = None

        if player_health_percent < 0.1:
            if self.__player_current_img != imageTkManager.NGUYEN_ZOMBIE_IMG_TK:
                img = imageTkManager.NGUYEN_ZOMBIE_IMG_TK
                self.__player_current_img = imageTkManager.NGUYEN_ZOMBIE_IMG_TK
        elif player_health_percent < 0.6:
            if self.__player_current_img != imageTkManager.NGUYEN_NORMAL_IMG_TK:
                img = imageTkManager.NGUYEN_NORMAL_IMG_TK
                self.__player_current_img = imageTkManager.NGUYEN_NORMAL_IMG_TK
        else:
            if self.__player_current_img != imageTkManager.NGUYEN_SAVIOR_IMG_TK:
                img = imageTkManager.NGUYEN_SAVIOR_IMG_TK
                self.__player_current_img = imageTkManager.NGUYEN_SAVIOR_IMG_TK
        
        if img is not None:
            self.__canvas.delete(self.__player_icon_id)
            self.__player_icon_id = self.__canvas.create_image(self.__upleft_corner[0] + 5, 
                            self.__upleft_corner[0] + 5,
                            anchor=NW,
                            image=img)
        
    def draw_health_points(self):
        """Dessine les points de vie
        """
        player = game.GAME.get_world().get_player()
        player_health = player.get_health()

        self.__health_id_imgs = fontManager.write_text(self.__canvas, 
                               "PV: " + str(player_health), 
                               self.__upleft_corner + Vec2D(100, 10),
                               3)
        
    def draw_player_pos(self):
        """Dessine la position du joueur
        """
        player = game.GAME.get_world().get_player()
        player_pos = player.get_pos()

        self.__pos_x_id_imgs = fontManager.write_text(self.__canvas, 
                               f"X: {player_pos[0]:.2f}", 
                               self.__upleft_corner + Vec2D(100, 25),
                               3)
        self.__pos_y_id_imgs = fontManager.write_text(self.__canvas, 
                               f"Y: {player_pos[1]:.2f}", 
                               self.__upleft_corner + Vec2D(100, 40),
                               3)

    def draw_player_rot(self):
        """Dessine la rotation du joueur
        """
        player = game.GAME.get_world().get_player()
        player_rot = player.get_rotation()

        self.__rot_id_imgs = fontManager.write_text(self.__canvas, 
                               f"rot: {player_rot}", 
                               self.__upleft_corner + Vec2D(100, 55),
                               3)
        
    def draw_player_score(self):
        """Dessine le score du joueur
        """
        player_score = game.GAME.get_world().get_player().get_score()

        self.__score_imgs = fontManager.write_text(self.__canvas, 
                                                   f"Score: {player_score}", 
                                                   self.__upleft_corner + Vec2D(100, 70),
                                                   3)

    def draw_player_ammo(self):
        """Dessine le nombre de balles du joueur
        """
        player_ammo = game.GAME.get_world().get_player().get_ammo()

        self.__ammo_imgs = fontManager.write_text(self.__canvas, 
                                                f"Ammo: {player_ammo}", 
                                                self.__upleft_corner + Vec2D(100, 85), 
                                                3)


    def on_player_move_event(self, dxy:Vec2D):
        """Mise a jour de la position

        Args:
            dxy (Vec2D): dxy
        """
        for pos_id_img in self.__pos_x_id_imgs:
            self.__canvas.delete(pos_id_img)
        self.__pos_x_id_imgs.clear()
        for pos_id_img in self.__pos_y_id_imgs:
            self.__canvas.delete(pos_id_img)
        self.__pos_y_id_imgs.clear()

        self.draw_player_pos()

    def on_player_rot_event(self):
        """Mise à jour de la rotation
        """
        for rot_id_img in self.__rot_id_imgs:
            self.__canvas.delete(rot_id_img)
        self.__rot_id_imgs.clear()

        self.draw_player_rot()

    def on_player_get_hit(self):
        """Mise à jour de la vie
        """
        for health_id_img in self.__health_id_imgs:
            self.__canvas.delete(health_id_img)
        self.__health_id_imgs.clear()

        self.draw_health_points()

    def on_player_score_change_event(self):
        """Mise à jour du score
        """
        for score_img in self.__score_imgs:
            self.__canvas.delete(score_img)
        self.__score_imgs.clear()

        self.draw_player_score()
    
    def on_player_use_ammo(self):
        """Mise  à jour des munitions
        """
        for ammo_img in self.__ammo_imgs:
            self.__canvas.delete(ammo_img)
        self.__ammo_imgs.clear()

        self.draw_player_ammo()
   