from math import atan2, pi, tan, radians, degrees
from typing import List

import logic.utils.mathUtils as mathUtils
from logic.entity.alien import Alien
from logic.entity.player import Player
from logic.utils.vec2D import Vec2D
from logic.world.blockType import BlockType

WORLD_DIM_X = 16
WORLD_DIM_Y = 16


class World:
    """
    La classe World permet de manipuler tous les objets quelle
    contient comme les entités
    """

    def __init__(self, world_matrix: List[List[BlockType]]):
        self.world_matrix = world_matrix

        self.__aliens = []
        self.__player = None

    def spawn_player(self, position: Vec2D, rotation: float) -> Player:
        """
        Fais apparaitre un joueur
        """
        # Impossible si il y a déjà un joueur
        if self.__player != None:
            return

        player = Player(world=self, position=position, rotation=rotation)
        self.__player = player
        return player

    def get_player(self) -> Player:
        """
        Renvoie le joueur
        """
        return self.__player
    
    def spawn_alien(self, position: Vec2D, rotation: float) -> Alien:
        alien = Alien(world=self, position=position, rotation=rotation)
        self.__aliens.append(alien)

        return alien

    def get_aliens(self) -> List[Alien]:
        """Renvoie la liste des aliens du jeu

        Returns:
            List[Alien]: Liste des aliens du monde
        """
        return self.__aliens

    def is_wall_between_entities(self, pos_1: Vec2D, pos_2: Vec2D):
        """Permet de savoir s'il existe un mur entre deux position
        du monde

        Args:
            pos_1 (Vec2D): position A
            pos_2 (Vec2D): position B

        Returns:
            bool: True s'il existe un mur entre deux positions du monde, False sinon
        """
        delta_xy = pos_2 - pos_1

        # Calcul de l'angle en radians
        angle_rad = atan2(delta_xy[1], delta_xy[0])

        # Conversion en degrés
        alpha = degrees(angle_rad)
        distance_to_next_wall, _, _ = self.get_next_wall_distance(pos_1, alpha)
        distance_to_alien = pos_2.distance(pos_1)

        return distance_to_alien > distance_to_next_wall

    def get_next_wall_distance(self, player_pos: Vec2D, alpha: float):
        """
        Renvoie 
            - la distance entre le joueur et le prochain mur touché avec l'angle alpha
            - Le pourcentage de mur touché
        """
        alpha %= 360
        x = player_pos[0]
        y = player_pos[1]

        if alpha % 90 == 0:
            alpha += 1

        tan_alpha = tan(alpha * pi / 180)

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
            if div < dih:  # On gère l'intersection verticale
                if self.world_matrix[int(ivy)][int(ivx + magic_v)] == BlockType.WALL:
                    return div, (ivy % 1), (ivy, ivx + magic_v)
                ivx += to_add_vx
                ivy += to_add_vy
                div += distance_to_add_v
            else:  # On gère l'intersection horizontale
                if self.world_matrix[int(ihy + magic_h)][int(ihx)] == BlockType.WALL:
                    return dih, (ihx % 1), (ihy + magic_h, ihx)
                ihx += to_add_hx
                ihy += to_add_hy
                dih += distance_to_add_h
