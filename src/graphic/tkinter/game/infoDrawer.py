from tkinter import Canvas, Tk

from graphic.tkinter.game.profile import Profile
from graphic.tkinter.game.minimapFont import MinimapFont

from logic.utils.vec2D import Vec2D
import logic.game.option as option

class InfoDrawer(Canvas):

    def __init__(self, master:Tk):
        super().__init__(master=master, 
                        width=option.OPTION.get_drawer_dimensions()[0], 
                        height=option.OPTION.get_drawer_dimensions()[1])
        super().pack(side="right")
        self.__minimap = MinimapFont(self)
        self.__profile = Profile(self)
        
    def draw(self):
        self.__minimap.draw()
        self.__profile.draw()

    def on_player_rot_event(self):
        self.__minimap.on_player_rot_event()
        self.__profile.on_player_rot_event()

    def on_player_move_event(self, dxy:Vec2D):
        self.__minimap.on_player_move_event(dxy)
        self.__profile.on_player_move_event(dxy)