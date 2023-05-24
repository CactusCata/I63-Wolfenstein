from tkinter import Canvas, Tk, NW

from graphic.tkinter.game.profile import Profile
from graphic.tkinter.game.minimapFont import MinimapFont

from logic.utils.vec2D import Vec2D
import logic.game.option as option
import logic.imagetk.imageTkManager as imageTkManager

class InfoDrawer(Canvas):
    """Classe qui affiche les informations du joueur et la minimap

    Args:
        Canvas (_type_): classe mère
    """

    def __init__(self, master:Tk):
        """Constructeur

        Args:
            master (Tk): Fenetre Tkinter
        """
        super().__init__(master=master, 
                        width=option.OPTION.get_info_dimensions()[0], 
                        height=option.OPTION.get_info_dimensions()[1])
        super().pack(side="right")
        self.__minimap = MinimapFont(self)
        self.__profile = Profile(self)
        
    def draw(self):
        """Dessine les éléments de Info
        """
        super().create_image(0, 
                          0,
                          anchor=NW,
                          image=imageTkManager.PROFIL_FONT_IMG_TK)
        self.__minimap.draw()
        self.__profile.draw()

    def on_player_rot_event(self):
        """Dessine les éléments de Info
        """
        self.__minimap.on_player_rot_event()
        self.__profile.on_player_rot_event()

    def on_player_move_event(self, dxy:Vec2D):
        """Dessine les éléments de Info
        """
        self.__minimap.on_player_move_event(dxy)
        self.__profile.on_player_move_event(dxy)

    def on_player_score_change_event(self):
        """Dessine les éléments de Info
        """
        self.__profile.on_player_score_change_event()

    def on_player_use_ammo_event(self):
        """Dessine les éléments de Info
        """
        self.__profile.on_player_use_ammo()

    def on_entities_move_event(self):
        """Dessine les éléments de Info
        """
        self.__minimap.on_entities_move_event()

    def on_player_get_hit(self):
        """Dessine les éléments de Info
        """
        self.__profile.on_player_get_hit()
        self.__profile.draw_player_icon()