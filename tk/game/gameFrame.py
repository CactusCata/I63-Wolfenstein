from tkinter import Tk, Canvas
from utils.vec2D import Vec2D
from utils.color import Color
import game.option as option
from game.game import Game
from entity.player import Player, PLAYER_SIZE_X, PLAYER_SIZE_Y, PLAYER_STEP_SIZE
from world.blockType import BlockType
from minimap.minimap import Minimap
from math import cos, sin, pi
from world.world import WORLD_DIM_X, WORLD_DIM_Y
from game.gameDrawer import GameDrawer

import utils.tkUtils as tkUtils


GAME_NAME = "Wolfenstein 2.5D"

class GameFrame:

    def __init__(self, enable_minimap=True):
        self.__root = Tk()
        self.__root.title(GAME_NAME)
        tkUtils.place_window(self.__root, option.OPTION.get_window_dimensions())
        tkUtils.lock_window_dimensions(self.__root, option.OPTION.get_window_dimensions())

        self.__canvas_game = Canvas(self.__root, width=option.OPTION.get_window_dimensions()[0], height=option.OPTION.get_window_dimensions()[1])
        self.__canvas_game.pack()

        self.__minimap = None

        self.__game = Game()

        self.__game_drawer = GameDrawer(self.__canvas_game, self.__game)
        self.__player = self.__game.get_world().spawn_player(position=Vec2D(9.5, 9.5), rotation=110)
        self.__root.bind('z', lambda event: self.move_player(+PLAYER_STEP_SIZE))
        self.__root.bind('q', lambda event: self.rotate_player(+3))
        self.__root.bind('s', lambda event: self.move_player(-PLAYER_STEP_SIZE))
        self.__root.bind('d', lambda event: self.rotate_player(-3))

    def run(self):
        self.__root.mainloop()

    def rotate_player(self, drotation:float):
        self.__player.add_rotation(drotation)
        self.__minimap.clear_all()
        self.__game_drawer.draw()
        self.__minimap.draw_minimap()
        #self.__minimap.update_minimap_player_eyes(drotation=drotation)
        #self.__minimap.draw_beams()

    def move_player(self, step:int):
        dxy = Vec2D(
            cos(self.__player.get_rotation() * pi / 180) * step, 
            sin(self.__player.get_rotation() * pi / 180) * step
        )

        player_square = (
            int(self.__player.get_pos()[0] + dxy[0] - 1/2 * PLAYER_SIZE_X),
            int(self.__player.get_pos()[1] + dxy[1] - 1/2 * PLAYER_SIZE_Y),
            int(self.__player.get_pos()[0] + dxy[0] + 1/2 * PLAYER_SIZE_X),
            int(self.__player.get_pos()[1] + dxy[1] + 1/2 * PLAYER_SIZE_Y)
        )

        
        if player_square[0] != player_square[2] or player_square[1] != player_square[3]: # Le joueur a passé une ligne
            rect = None
            if dxy[0] > 0:
                rect = (player_square[0] + 1, player_square[1])
            elif dxy[0] < 0:
                rect = (player_square[0], player_square[1])
            if self.__game.get_world().world_matrix[rect[1]][rect[0]] == BlockType.WALL:
                return
            if dxy[1] > 0:
                rect = (player_square[0], player_square[1])
            else:
                rect = (player_square[0], player_square[1])

            if self.__game.get_world().world_matrix[rect[1]][rect[0]] == BlockType.WALL:
                return

    
        
        self.__player.move(dxy)
        self.__minimap.clear_all()
        self.__game_drawer.draw()
        self.__minimap.draw_minimap()
        #self.__minimap.update_minimap_player_move(dxy)
        #self.__minimap.draw_beams()
        

    def enable_minimap(self, upleft_corner:Vec2D, downright_corner:Vec2D):
        self.__minimap = Minimap(self.__game, self.__canvas_game, upleft_corner, downright_corner)
        self.__minimap.draw_minimap()

    def draw_pixel(self, vec2d:Vec2D, color:Color=None):
        """
        Dessine un pixel
        """
        if color == None:
            self.__canvas_game.create_rectangle(vec2d[0], vec2d[1], vec2d[0] + 1, vec2d[1] + 1)
        else:
            self.__canvas_game.create_rectangle(vec2d[0], vec2d[1], vec2d[0] + 1, vec2d[1] + 1, fill=color)
