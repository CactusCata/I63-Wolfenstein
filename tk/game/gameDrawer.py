from tkinter import Canvas
from game.game import Game
from math import tan, cos, sin, pi, sqrt, exp
import game.option as option
from world.blockType import BlockType
from utils.vec2D import Vec2D
import utils.mathUtils as mathUtils

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
        
        h = 0.7

        for col in range(screen_width):
            angle = (col * fov) / screen_width + player_rotation - 1/2 * fov
            distance = self.get_next_wall_distance(angle)
            
            # fix the "lentille effet"
            distance = distance * cos((player_rotation - angle) * pi / 180)
            
            r = h * (virtual_distance / distance)
            #self.__canvas.create_rectangle(col, (screen_height - r) // 2, col+1, (screen_height - r) // 2 + 1)
            #self.__canvas.create_rectangle(col, (screen_height + r) // 2, col+1, (screen_height + r) // 2 + 1)
            self.__canvas.create_line(col, (screen_height - r) // 2, col+1, (screen_height + r) // 2, fill=self.get_color_from_distance(distance))

    
    def get_color_from_distance(self, distance):
        res = 255 - int(255 * (1 - exp(-distance/3)))
        return f"#{res:02X}{res:02X}{res:02X}"
    
    def get_next_wall_distance(self, alpha):
        alpha %= 360
        tan_alpha = tan(alpha * pi / 180)
        world_matrix = self.__game.get_world().world_matrix
        player_pos = self.__game.get_world().get_player().get_pos()
        x = player_pos[0]
        y = player_pos[1]

        ivx = 0
        ivy = 0
        ihx = 0
        ihy = 0
        coef_v = 1
        coef_h = 1

        if alpha < 90:
            ivx = int(x) + 1
            ivy = y + abs(x - ivx) * tan_alpha
            ihy = int(y) + 1
            ihx = x + abs(y - ihy) / tan_alpha
        elif alpha < 180:
            ivx = int(x)
            ivy = y + abs(x - ivx) * tan_alpha * -1
            ihy = int(y) + 1
            ihx = x + abs(y - ihy) / tan_alpha
            coef_v = -1
        elif alpha < 270:
            ivx = int(x)
            ivy = y + abs(x - ivx) * tan_alpha * -1
            ihy = int(y)
            ihx = x + abs(y - ihy) / tan_alpha * -1
            coef_v = -1
            coef_h = -1
        else:
            ivx = int(x) + 1
            ivy = y + abs(x - ivx) * tan_alpha
            ihy = int(y)
            ihx = x + abs(y - ihy) / tan_alpha * -1
            coef_h = -1

        div = mathUtils.euclidian_distance(x, y, ivx, ivy)
        dih = mathUtils.euclidian_distance(x, y, ihx, ihy)
        
        

        while True:
            if div < dih: # On gère l'intersection verticale
                if coef_v == 1 and world_matrix[int(ivy)][int(ivx)] == BlockType.WALL:
                    return div
                elif coef_v == -1 and world_matrix[int(ivy)][int(ivx - 1)] == BlockType.WALL:
                    return div
                ivx += coef_v
                ivy += coef_v * tan_alpha
                div = mathUtils.euclidian_distance(x, y, ivx, ivy)
            else: # On gère l'intersection horizontale
                if coef_h == 1 and world_matrix[int(ihy)][int(ihx)] == BlockType.WALL:
                    return dih
                elif coef_h == -1 and world_matrix[int(ihy - 1)][int(ihx)] == BlockType.WALL:
                    return dih
                ihx += coef_h / tan_alpha
                ihy += coef_h
                dih = mathUtils.euclidian_distance(x, y, ihx, ihy)

    
    """
    def get_next_wall_distance(self, alpha):
        world_matrix = self.__game.get_world().world_matrix
        player_pos = self.__game.get_world().get_player().get_pos()
        x = player_pos[0]
        y = player_pos[1]
        
        vx = cos(alpha * pi / 180) / 64
        vy = sin(alpha * pi / 180) / 64

        while True:
            if world_matrix[int(y)][int(x)] == BlockType.WALL:
                return sqrt((x - player_pos[0])**2 + (y - player_pos[1])**2)
            else:
                x += vx
                y += vy
    """



    def draw_background(self):
        window_dimensions = option.OPTION.get_window_dimensions()
        self.__canvas.create_rectangle(0, 0, window_dimensions[0], window_dimensions[1] // 2, fill="blue")
        self.__canvas.create_rectangle(0, window_dimensions[1] // 2, window_dimensions[0], window_dimensions[1], fill="gray")