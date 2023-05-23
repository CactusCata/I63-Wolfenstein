from tkinter import Tk, BOTH, YES, Frame, BOTTOM, TOP, RIGHT
from math import cos, sin, pi

import graphic.tkinter.utils.tkUtils as tkUtils
from graphic.tkinter.tkDrawer import TkDrawner
from graphic.info.infoDrawer import InfoDrawer
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

        # Infos
        self.info_drawer = InfoDrawer(master=self.__root)
        self.info_drawer.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Interface Tkinter
        frame_tkinter = Frame(master=self.__root)
        frame_tkinter.pack(side=TOP)
        self.__tkinter_drawer = TkDrawner(master=frame_tkinter)

        # Interface OpenGL
        self.__ogl_drawer = OGLDrawer(self.__root)
        self.__ogl_drawer.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.__ogl_drawer.animate = 1
        self.__ogl_drawer.after(100, self.__ogl_drawer.printContext)

        self.start_ia_aliens()

    def run(self):
        # First draw Tkinter interface
        self.__tkinter_drawer.init_draw()
        self.info_drawer.draw()

        self.__root.after(1000, self.redraw)

        self.__root.mainloop()

    def redraw(self):
        self.__tkinter_drawer.redraw()
        self.__root.after(0, self.redraw)
        

    def rotate_player(self, drotation:float):
        self.__player.add_rotation(drotation)

        self.info_drawer.on_player_rot_event()
        self.__tkinter_drawer.on_player_rot_event()

    def move_player(self, step_size:int):
        dxy = Vec2D(
            cos(self.__player.get_rotation() * pi / 180) * step_size, 
            sin(self.__player.get_rotation() * pi / 180) * step_size
        )

        if self.__player.can_move(dxy):
            self.__player.move(dxy)
            self.info_drawer.on_player_move_event(dxy)
            self.__tkinter_drawer.on_player_move_event(dxy)

    def start_ia_aliens(self):
        pass
        #print("to do logic here")
        #self.__root.after(1000, self.start_logic)
