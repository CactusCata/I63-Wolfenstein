from tkinter import Tk, BOTH, YES, Frame, BOTTOM, TOP, RIGHT
from math import cos, sin, pi

import graphic.tkinter.utils.tkUtils as tkUtils
from graphic.tkinter.tkDrawer import TkDrawner
from graphic.info.infoDrawer import InfoDrawer
from graphic.opengl.oglDrawer import OGLDrawer

import logic.game.option as option
import logic.game.game as game
from logic.utils.vec2D import Vec2D
from logic.entity.player import PLAYER_STEP_SIZE, PLAYER_DAMAGE
from logic.entity.alien import ALIEN_MOVE_FREQUENCY_MS


GAME_NAME = "Wolfenstein 2.5D"

class DrawerManager:
    """Manager de la partie vue
    """

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
        self.__root.bind('<Button-1>', lambda event: self.player_shoot())

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

    def run(self):
        """Dessine les elements à l'écran
        (A appeler qu'une seule fois)
        """
        # First draw Tkinter interface
        self.__tkinter_drawer.init_draw()
        self.info_drawer.draw()

        self.__root.after(1000, self.alien_action)

        self.__root.mainloop()

    def redraw(self):
        """Redessine les elements à l'écran
        """
        self.__tkinter_drawer.redraw()

    def alien_action(self):
        """Autorise tous les aliens à se déplacer et à effectuer une attaque
        """
        for alien in game.GAME.get_world().get_aliens():
            alien.move()
            alien.try_attack()
        
        self.info_drawer.on_entities_move_event()
        self.info_drawer.on_player_get_hit()
        self.redraw()
        self.__root.after(ALIEN_MOVE_FREQUENCY_MS, self.alien_action)
        

    def rotate_player(self, drotation:float):
        """Fonction appelée lorsque le joueur souhaite se tourner

        Args:
            drotation (float): delta rotation
        """
        self.__player.add_rotation(drotation)

        self.info_drawer.on_player_rot_event()
        self.__tkinter_drawer.on_player_rot_event()

    def move_player(self, step_size:int):
        """Fonction appelée lorsque le joueur souhaite se déplacer

        Args:
            step_size (int): taille du pas de déplacement
        """
        dxy = Vec2D(
            cos(self.__player.get_rotation() * pi / 180) * step_size, 
            sin(self.__player.get_rotation() * pi / 180) * step_size
        )

        if self.__player.can_move(dxy):
            self.__player.move(dxy)
            self.info_drawer.on_player_move_event(dxy)
            self.__tkinter_drawer.on_player_move_event(dxy)

    def player_shoot(self):
        """Simule le tir du joueur
        """
        if not self.__player.can_shoot():
            return

        
        self.__player.use_ammo()

        alien_aimed = self.__player.get_alien_aimed()
        if alien_aimed != None:
            alien_aimed.add_damage(PLAYER_DAMAGE)

            if alien_aimed.get_health() == 0:
                game.GAME.get_world().get_aliens().remove(alien_aimed)
                self.__player.reset_alien_aimed()
                self.__player.increase_score()
                self.__player.add_ammo(4)
                self.info_drawer.on_player_score_change_event()

        
        self.info_drawer.on_player_use_ammo_event()
