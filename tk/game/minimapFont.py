from utils.vec2D import Vec2D
from tkinter import Canvas
from world.world import WORLD_DIM_X, WORLD_DIM_Y
from game.game import Game
from math import sin, cos, tan, pi
from entity.player import PLAYER_SIZE_X, PLAYER_SIZE_Y
from world.blockType import BlockType
import game.option as option
import utils.mathUtils as mathUtils
from utils.tkUtils import ONE_USE_TAG_TUPLE, DEFINITIVE_USE_TAG_TUPLE_2

class MinimapFont:

    def __init__(self, game:Game, canvas:Canvas, upleft_corner:Vec2D, downright_corner:Vec2D):
        self.__game = game
        self.__canvas = canvas
        self.__upleft_corner = upleft_corner
        self.__downright_corner = downright_corner

        self.__to_add_x = (downright_corner[0] - upleft_corner[0]) / WORLD_DIM_X
        self.__to_add_y = (downright_corner[1] - upleft_corner[1]) / WORLD_DIM_Y

        self.__player_draw_id = -1

    def get_player_hitbox_tk(self):
        return self.__canvas.coords(self.__player_draw_id)

    def draw(self):
        self.draw_minimap_background()
        self.draw_minimap_grid()
        self.draw_minimap_blocks()
        self.draw_minimap_player()
        self.draw_beams()

    def redraw(self):
        self.draw_beams()

    def draw_minimap_background(self):
        self.__canvas.create_rectangle(self.__upleft_corner[0], 
                                       self.__upleft_corner[1], 
                                       self.__downright_corner[0], 
                                       self.__downright_corner[1],
                                       fill="white",
                                       tags=DEFINITIVE_USE_TAG_TUPLE_2
                                       )

    #####################
    #   Dessin joueur   #
    #####################
    def draw_minimap_player(self):
        player = self.__game.get_world().get_player()
        player_pos = player.get_pos()
        self.__player_draw_id = self.__canvas.create_oval((player_pos[0] - 1/2 * PLAYER_SIZE_X) * self.__to_add_x + self.__upleft_corner[0], 
                                    (player_pos[1] - 1/2 * PLAYER_SIZE_Y) * self.__to_add_y + self.__upleft_corner[1], 
                                    (player_pos[0] + 1/2 * PLAYER_SIZE_X) * self.__to_add_x + self.__upleft_corner[0], 
                                    (player_pos[1] + 1/2 * PLAYER_SIZE_Y) * self.__to_add_y + self.__upleft_corner[1], 
                                    fill="red",
                                    tags=DEFINITIVE_USE_TAG_TUPLE_2)
        
    def update_minimap_player_move(self, dxy:Vec2D):
        if self.__player_draw_id == -1:
            self.draw_minimap_player()
        self.__canvas.move(self.__player_draw_id, dxy[0] * self.__to_add_x, dxy[1] * self.__to_add_y)
        
    ####################
    #   Dessin blocs   #
    ####################
    def draw_minimap_blocks(self):
        current_y = self.__upleft_corner[1]
        world = self.__game.get_world()
        for y in range(WORLD_DIM_Y):
            current_x = self.__upleft_corner[0]
            for x in range(WORLD_DIM_X):
                block_type = world.world_matrix[y][x]
                block_type.value[2](self.__canvas, 
                                    Vec2D(current_x, current_y),
                                    Vec2D(current_x + self.__to_add_x, current_y + self.__to_add_y))
                current_x += self.__to_add_x
            current_y += self.__to_add_y

    #####################
    #   Dessin grille   #
    #####################
    def draw_minimap_grid(self):
        current_y = self.__upleft_corner[1]
        for line in range(WORLD_DIM_Y + 1):
            self.__canvas.create_line(self.__upleft_corner[0], 
                                           current_y,
                                           self.__downright_corner[0],
                                           current_y,
                                           tags=DEFINITIVE_USE_TAG_TUPLE_2)
            current_y += self.__to_add_y

        current_x = self.__upleft_corner[0]
        for col in range(WORLD_DIM_X + 1):
            self.__canvas.create_line(current_x, 
                                           self.__upleft_corner[1], 
                                           current_x, 
                                           self.__downright_corner[1],
                                           tags=DEFINITIVE_USE_TAG_TUPLE_2)
            current_x += self.__to_add_x

    #################
    #   Dessin dda  #
    #################
    def draw_beams(self):
        fov = option.OPTION.get_fov()
        player_rotation = self.__game.get_world().get_player().get_rotation()
        #self.draw_beam(player_rotation - fov // 2)
        self.draw_beam(player_rotation)
        #self.draw_beam(player_rotation + fov // 2)

    def draw_beam(self, alpha):
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
                    self.draw_line(player_pos, Vec2D(ivx, ivy), color="blue")
                    return
                elif coef_v == -1 and world_matrix[int(ivy)][int(ivx - 1)] == BlockType.WALL:
                    self.draw_line(player_pos, Vec2D(ivx, ivy), color="blue")
                    return
                ivx += coef_v
                ivy += coef_v * tan_alpha
                div = mathUtils.euclidian_distance(x, y, ivx, ivy)
            else: # On gère l'intersection horizontale
                if coef_h == 1 and world_matrix[int(ihy)][int(ihx)] == BlockType.WALL:
                    self.draw_line(player_pos, Vec2D(ihx, ihy), color="blue")
                    return
                elif coef_h == -1 and world_matrix[int(ihy - 1)][int(ihx)] == BlockType.WALL:
                    self.draw_line(player_pos, Vec2D(ihx, ihy), color="blue")
                    return
                ihx += coef_h / tan_alpha
                ihy += coef_h
                dih = mathUtils.euclidian_distance(x, y, ihx, ihy)




        """
        
        vx = cos(alpha * pi / 180) / 16
        vy = sin(alpha * pi / 180) / 16

        while True:
            if world_matrix[int(y)][int(x)] == BlockType.WALL:
                break
            else:
                x += vx
                y += vy


        beam_id = self.draw_line(player_pos, Vec2D(x, y), color="blue")
        self.__beams_draw_id.append(beam_id)
        """

    #############
    #   Others  #
    #############
    def draw_line(self, map_space_p1:Vec2D, map_space_p2:Vec2D, color:str=None):
        return self.__canvas.create_line(map_space_p1[0] * self.__to_add_x + self.__upleft_corner[0], 
                                         map_space_p1[1] * self.__to_add_y + self.__upleft_corner[1],
                                         map_space_p2[0] * self.__to_add_x + self.__upleft_corner[0],
                                         map_space_p2[1] * self.__to_add_y + self.__upleft_corner[1],
                                         fill=color,
                                         tags=ONE_USE_TAG_TUPLE)