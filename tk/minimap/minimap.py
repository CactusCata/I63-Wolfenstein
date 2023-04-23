from utils.vec2D import Vec2D
from tkinter import Canvas
from world.world import WORLD_DIM_X, WORLD_DIM_Y
from game.game import Game
from math import sin, cos, tan, pi
from entity.player import PLAYER_SIZE_X, PLAYER_SIZE_Y
from world.blockType import BlockType
import game.option as option

class Minimap:

    def __init__(self, game:Game, canvas:Canvas, upleft_corner:Vec2D, downright_corner:Vec2D):
        self.__game = game
        self.__canvas = canvas
        self.__upleft_corner = upleft_corner
        self.__downright_corner = downright_corner

        self.__to_add_x = (downright_corner[0] - upleft_corner[0]) / WORLD_DIM_X
        self.__to_add_y = (downright_corner[1] - upleft_corner[1]) / WORLD_DIM_Y

        self.__player_draw_id = -1
        self.__player_eyes_id = [-1, -1]
        self.__grid_lines_draw_id = []
        self.__blocks_draw_id = []
        self.__beams_draw_id = []

    def get_player_hitbox_tk(self):
        return self.__canvas.coords(self.__player_draw_id)

    def draw_minimap(self):
        self.draw_minimap_background()
        self.draw_minimap_grid()
        self.draw_minimap_blocks()
        self.draw_minimap_player()
        self.draw_minimap_player_eyes()
        self.draw_beams()

    def clear_all(self):
        self.__canvas.delete("all")
        self.__grid_lines_draw_id.clear()
        self.__blocks_draw_id.clear()
        self.__beams_draw_id.clear()

    def draw_minimap_background(self):
        self.__canvas.create_rectangle(self.__upleft_corner[0], 
                                       self.__upleft_corner[1], 
                                       self.__downright_corner[0], 
                                       self.__downright_corner[1],
                                       fill="white"
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
                                    fill="red")
        
    def draw_minimap_player_eyes(self):
        player = self.__game.get_world().get_player()
        pos_eye_left_x = (player.get_pos()[0] + 1/2 + 0.8 * cos((player.get_rotation() * pi / 180) + pi/6)) * self.__to_add_x + self.__upleft_corner[0]
        pos_eye_left_y = (player.get_pos()[1] + 1/2 + 0.8 * sin((player.get_rotation() * pi / 180) + pi/6)) * self.__to_add_y + self.__upleft_corner[1]
        pos_eye_right_x = (player.get_pos()[0] + 1/2 + 0.8 * cos((player.get_rotation() * pi / 180) - pi/6)) * self.__to_add_x + self.__upleft_corner[0]
        pos_eye_right_y = (player.get_pos()[1] + 1/2 + 0.8 * sin((player.get_rotation() * pi / 180) - pi/6)) * self.__to_add_y + self.__upleft_corner[1]
        self.__player_eyes_id[0] = self.__canvas.create_rectangle(pos_eye_left_x, pos_eye_left_y, pos_eye_left_x + 1, pos_eye_left_y + 1)
        self.__player_eyes_id[1] = self.__canvas.create_rectangle(pos_eye_right_x, pos_eye_right_y, pos_eye_right_x + 1, pos_eye_right_y + 1)
        
    def update_minimap_player_move(self, dxy:Vec2D):
        if self.__player_draw_id == -1:
            self.draw_minimap_player()
        self.__canvas.move(self.__player_draw_id, dxy[0] * self.__to_add_x, dxy[1] * self.__to_add_y)
        self.update_minimap_player_eyes(dxy=dxy)
        
        
    def update_minimap_player_eyes(self, dxy:Vec2D=Vec2D(0, 0), drotation=0.0):
        if self.__player_eyes_id == [-1, -1]:
            self.draw_minimap_player_eyes()

        if dxy != Vec2D(0, 0):
            self.__canvas.move(self.__player_eyes_id[0], dxy[0] * self.__to_add_x, dxy[1] * self.__to_add_y)
            self.__canvas.move(self.__player_eyes_id[1], dxy[0] * self.__to_add_x, dxy[1] * self.__to_add_y)
        
        if drotation != 0.0:
            self.__canvas.delete(self.__player_eyes_id[0])
            self.__canvas.delete(self.__player_eyes_id[1])
            self.draw_minimap_player_eyes()
        
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
                block_id = block_type.value[2](self.__canvas, 
                                    Vec2D(current_x, current_y),
                                    Vec2D(current_x + self.__to_add_x, current_y + self.__to_add_y))
                self.__blocks_draw_id.append(block_id)
                current_x += self.__to_add_x
            current_y += self.__to_add_y

    #####################
    #   Dessin grille   #
    #####################
    def draw_minimap_grid(self):
        current_y = self.__upleft_corner[1]
        for line in range(WORLD_DIM_Y + 1):
            line_id = self.__canvas.create_line(self.__upleft_corner[0], 
                                           current_y,
                                           self.__downright_corner[0],
                                           current_y)
            self.__grid_lines_draw_id.append(line_id)
            current_y += self.__to_add_y

        current_x = self.__upleft_corner[0]
        for col in range(WORLD_DIM_X + 1):
            col_id = self.__canvas.create_line(current_x, 
                                           self.__upleft_corner[1], 
                                           current_x, 
                                           self.__downright_corner[1])
            self.__grid_lines_draw_id.append(col_id)
            current_x += self.__to_add_x

    #################
    #   Dessin dda  #
    #################
    def draw_beams(self):
        self.clear_beams()
        fov = option.OPTION.get_fov()
        player_rotation = self.__game.get_world().get_player().get_rotation()
        self.draw_beam(player_rotation - fov // 2)
        self.draw_beam(player_rotation)
        self.draw_beam(player_rotation + fov // 2)

    def draw_beam(self, alpha):
        world_matrix = self.__game.get_world().world_matrix
        player_pos = self.__game.get_world().get_player().get_pos()
        x = player_pos[0]
        y = player_pos[1]
        
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

    def clear_beams(self):
        for beam_id in self.__beams_draw_id:
            self.__canvas.delete(beam_id)
        self.__beams_draw_id.clear()

    #############
    #   Others  #
    #############
    def draw_line(self, map_space_p1:Vec2D, map_space_p2:Vec2D, color:str=None):
        return self.__canvas.create_line(map_space_p1[0] * self.__to_add_x + self.__upleft_corner[0], 
                                         map_space_p1[1] * self.__to_add_y + self.__upleft_corner[1],
                                         map_space_p2[0] * self.__to_add_x + self.__upleft_corner[0],
                                         map_space_p2[1] * self.__to_add_y + self.__upleft_corner[1],
                                         fill=color)