from enum import Enum
from tkinter import Canvas
from utils.vec2D import Vec2D

def draw_mini_map_air(canvas:Canvas, upleft_corner:Vec2D, downright_corner:Vec2D):
    pass

def draw_mini_map_wall(canvas:Canvas, upleft_corner:Vec2D, downright_corner:Vec2D):
    canvas.create_rectangle(upleft_corner[0], upleft_corner[1], downright_corner[0], downright_corner[1], fill="black")

class BlockType(Enum):

    AIR = ("AIR", ' ', draw_mini_map_air)
    WALL = ("WALL", '+', draw_mini_map_wall)

    @staticmethod
    def get_block_type_from_char(block_char_representation:str):
        for block_type in BlockType:
            if block_type.value[1] == block_char_representation:
                return block_type
        return None

