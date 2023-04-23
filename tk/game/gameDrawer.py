from tkinter import Canvas
from game.game import Game
from math import tan, cos, sin, pi, sqrt, exp
import game.option as option
from world.blockType import BlockType
from utils.vec2D import Vec2D

class GameDrawer:

    def __init__(self, canvas:Canvas, game:Game):
        self.__canvas = canvas
        self.__game = game

    def draw(self):
        self.draw_background()

        fov = option.OPTION.get_fov()
        player_rotation = self.__game.get_world().get_player().get_rotation()
        screen_width = option.OPTION.get_window_dimensions()[0]
        screen_height = option.OPTION.get_window_dimensions()[1]
        virtual_distance = (screen_width / 2) / (tan((fov/2) * pi / 180))
        
        h = 1

        for col in range(screen_width):
            distance = self.get_next_wall_distance((col * fov * 1/2) / screen_width + player_rotation - 30/2)
            r = h * (virtual_distance / distance)
            #self.__canvas.create_rectangle(col, (screen_height - r) // 2, col+1, (screen_height - r) // 2 + 1)
            #self.__canvas.create_rectangle(col, (screen_height + r) // 2, col+1, (screen_height + r) // 2 + 1)
            self.__canvas.create_line(col, (screen_height - r) // 2, col+1, (screen_height + r) // 2, fill=self.get_color_from_distance(distance))

    def get_color_from_distance(self, distance):
        res = 255 - int(255 * (1 - exp(-distance/3)))
        return f"#{res:02X}{res:02X}{res:02X}"

    def get_next_wall_distance(self, alpha):
        world_matrix = self.__game.get_world().world_matrix
        player_pos = self.__game.get_world().get_player().get_pos()
        x = player_pos[0]
        y = player_pos[1]
        
        vx = cos(alpha * pi / 180) / 16
        vy = sin(alpha * pi / 180) / 16

        while True:
            if world_matrix[int(y)][int(x)] == BlockType.WALL:
                return sqrt((x - player_pos[0])**2 + (y - player_pos[1])**2)
            else:
                x += vx
                y += vy



    def draw_background(self):
        window_dimensions = option.OPTION.get_window_dimensions()
        self.__canvas.create_rectangle(0, 0, window_dimensions[0], window_dimensions[1] // 2, fill="blue")
        self.__canvas.create_rectangle(0, window_dimensions[1] // 2, window_dimensions[0], window_dimensions[1], fill="gray")