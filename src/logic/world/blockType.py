from enum import Enum
from tkinter import Canvas
from logic.utils.vec2D import Vec2D

from graphic.tkinter.utils.tkUtils import DEFINITIVE_USE_TAG_TUPLE_2

"""
Fichier permetant de dessiner les blocs dans la minimap
"""

def draw_mini_map_air(canvas:Canvas, upleft_corner:Vec2D, downright_corner:Vec2D):
    """Dessine un bloc d'air sur la minimap

    Args:
        canvas (Canvas): canvas de dessin
        upleft_corner (Vec2D): position en pixel en haut à gauche à dessiner
        downright_corner (Vec2D): position en pixel en bas à droite à dessiner
    """
    pass

def draw_mini_map_wall(canvas:Canvas, upleft_corner:Vec2D, downright_corner:Vec2D):
    """Dessine un bloc de mur sur la minimap

    Args:
        canvas (Canvas): canvas de dessin
        upleft_corner (Vec2D): position en pixel en haut à gauche à dessiner
        downright_corner (Vec2D): position en pixel en bas à droite à dessiner
    """
    canvas.create_rectangle(upleft_corner[0], upleft_corner[1], downright_corner[0], downright_corner[1], fill="black",
                                      tags=DEFINITIVE_USE_TAG_TUPLE_2)

class BlockType(Enum):
    """Liste tous les types de bloc du jeu

    Args:
        Enum (_type_): _description_

    Returns:
        _type_: _description_
    """

    AIR = ("AIR", ' ', draw_mini_map_air)
    WALL = ("WALL", '+', draw_mini_map_wall)

    @staticmethod
    def get_block_type_from_char(block_char_representation:str):
        for block_type in BlockType:
            if block_type.value[1] == block_char_representation:
                return block_type
        return None

