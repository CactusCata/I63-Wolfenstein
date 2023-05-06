from typing import List, TYPE_CHECKING
from math import atan2, pi, tan

from logic.world.blockType import BlockType
from logic.utils.vec2D import Vec2D
from logic.entity.player import Player
from logic.entity.alien import Alien
from logic.entity.entity import Entity
import logic.utils.mathUtils as mathUtils


WORLD_DIM_X = 16
WORLD_DIM_Y = 16

class World:

    def __init__(self, world_matrix:List[List[BlockType]]):
        self.world_matrix = world_matrix

        self.__aliens = []
        self.__player = None

    def spawn_player(self, position:Vec2D, rotation:float) -> Player:
        player = Player(world=self, position=position, rotation=rotation)
        self.__player = player
        return player

    def get_player(self) -> Player:
        return self.__player
    
    def spawn_alien(self, position:Vec2D, rotation:float) -> Player:
        alien = Alien(world=self, position=position, rotation=rotation)
        self.__aliens.append(alien)

    def get_aliens(self):
        return self.__aliens
    
        
    def is_wall_between_entities(self, pos_1:Vec2D, pos_2:Vec2D):
        delta_xy = pos_2 - pos_1

        # Calcul de l'angle en radians
        angle_rad = atan2(delta_xy[1], delta_xy[0])

        # Conversion en degrés
        alpha = angle_rad * 180 / pi
        distance_to_next_wall,_ = self.get_next_wall_distance(pos_1, alpha)
        distance_to_alien = delta_xy.distance(pos_1)

        return distance_to_alien > distance_to_next_wall


    def get_next_wall_distance(self, player_pos:Vec2D, alpha:float):
        """
        Renvoie 
            - la distance entre le joueur et le prochain mur touché avec l'angle alpha
            - Le pourcentage de mur touché
        """
        alpha %= 360
        tan_alpha = tan(alpha * pi / 180)
        x = player_pos[0]
        y = player_pos[1]

        ivx = 0
        ivy = 0
        ihx = 0
        ihy = 0
        coef_v = 1
        coef_h = 1
        magic_v = 0
        magic_h = 0

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
            magic_v = -1
        elif alpha < 270:
            ivx = int(x)
            ivy = y + abs(x - ivx) * tan_alpha * -1
            ihy = int(y)
            ihx = x + abs(y - ihy) / tan_alpha * -1
            coef_v = -1
            magic_v = -1
            coef_h = -1
            magic_h = -1
        else:
            ivx = int(x) + 1
            ivy = y + abs(x - ivx) * tan_alpha
            ihy = int(y)
            ihx = x + abs(y - ihy) / tan_alpha * -1
            coef_h = -1
            magic_h = -1

        div = mathUtils.euclidian_distance(x, y, ivx, ivy)
        dih = mathUtils.euclidian_distance(x, y, ihx, ihy)

        to_add_vx = coef_v
        to_add_vy = coef_v * tan_alpha
        to_add_hx = coef_h / tan_alpha
        to_add_hy = coef_h

        distance_to_add_v = mathUtils.euclidian_distance(ivx, ivy, ivx + to_add_vx, ivy + to_add_vy)
        distance_to_add_h = mathUtils.euclidian_distance(ihx, ihy, ihx + to_add_hx, ihy + to_add_hy)


        
        while True:
            if div < dih: # On gère l'intersection verticale
                if self.world_matrix[int(ivy)][int(ivx + magic_v)] == BlockType.WALL:
                    return div, (ivy % 1)
                ivx += to_add_vx
                ivy += to_add_vy
                div += distance_to_add_v
            else: # On gère l'intersection horizontale
                if self.world_matrix[int(ihy + magic_h)][int(ihx)] == BlockType.WALL:
                    return dih, (ihx % 1)
                ihx += to_add_hx
                ihy += to_add_hy
                dih += distance_to_add_h