from tkinter import Tk, BOTH, YES
from math import cos, sin, pi

import graphic.utils.tkUtils as tkUtils
from graphic.tkinter.tkDrawer import TkDrawner
from graphic.opengl.oglDrawer import OGLDrawer

import logic.game.option as option
import logic.game.game as game
from logic.utils.vec2D import Vec2D
from logic.entity.player import PLAYER_STEP_SIZE


GAME_NAME = "Wolfenstein 2.5D"

class DrawerManager:

    def __init__(self):
        self.__root = Tk()
        self.__root.title(GAME_NAME)

        self.__player = game.GAME.get_world().get_player()

        # Paramètres du root
        screen_dims = option.OPTION.get_window_dimensions()
        win_dims = Vec2D(screen_dims[0], screen_dims[1] * 2)
        tkUtils.place_window(self.__root, win_dims)
        tkUtils.lock_window_dimensions(self.__root, win_dims)

        # Bindings
        self.__root.bind('z', lambda event: self.move_player(+PLAYER_STEP_SIZE))
        self.__root.bind('d', lambda event: self.rotate_player(+3))
        self.__root.bind('s', lambda event: self.move_player(-PLAYER_STEP_SIZE))
        self.__root.bind('q', lambda event: self.rotate_player(-3))

        # Interface Tkinter
        self.__tkinter_drawer = TkDrawner(master=self.__root)
        self.__tkinter_drawer.pack()

        # Add minimap on Tkinter Interface
        minimap_ratio_width = 0.85
        minimap_ratio_height = 0.05
        minimap_pos = Vec2D(screen_dims[0] * minimap_ratio_width, screen_dims[1] * minimap_ratio_height)
        minimap_size = 100
        self.__tkinter_drawer.enable_minimap(minimap_pos, 
                                             Vec2D(minimap_pos[0] + minimap_size, 
                                                   minimap_pos[1] + minimap_size)
        )

        # First draw Tkinter interface
        self.__tkinter_drawer.init_draw()

        # Interface OpenGL
        self.__ogl_drawer = OGLDrawer(self.__root)
        self.__ogl_drawer.pack(fill=BOTH, expand=YES)
        self.__ogl_drawer.animate = 1
        self.__ogl_drawer.after(100, self.__ogl_drawer.printContext)
        
        self.__root.mainloop()

    def rotate_player(self, drotation:float):
        self.__player.add_rotation(drotation)

        self.__tkinter_drawer.redraw_rot()

    def move_player(self, step_size:int):
        dxy = Vec2D(
            cos(self.__player.get_rotation() * pi / 180) * step_size, 
            sin(self.__player.get_rotation() * pi / 180) * step_size
        )

        if self.__player.can_move(dxy):
            self.__player.move(dxy)
            self.__tkinter_drawer.redraw_move(dxy)
