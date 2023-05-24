from tkinter import Label
from typing import List

import numpy as np
import logic.game.option as option

from PIL import Image, ImageTk

class ZBuffer:

    """Classe qui permet d'afficher efficacement des
    dessins Tkinter
    """

    def __init__(self, container:Label):
        """Constructeur

        Args:
            container (Label): Conteneur dans lequel sera affiché le zbuffer
        """
        self.container = container
        self.img_tk = None
        window_dims = option.OPTION.get_window_dimensions()
        self.clear_buffer = np.zeros([window_dims[1], window_dims[0], 3], dtype=np.uint8)
        self.buffer = self.clear_buffer.copy()

    def set(self, x: int, y: int, color:List[int]):
        """Place un pixel

        Args:
            x (int): position en pixel de la largeur sur le zbuffer
            y (int): position en pixel de la hauteur sur le zbuffer 
            color (List[int]): Triplet (R,G,B)
        """
        self.buffer[y,x] = color

    def set_col(self, col:int, line_start:int, line_end:int, color:List[int]):
        """Place une colonne de pixel de la même valeur

        Args:
            col (int): colonne concernée
            line_start (int): ligne de départ
            line_end (int): ligne de fin
            color (List[int]): couleur
        """
        self.buffer[line_start:line_end,col] = color

    def set_line(self, line: int, col_start: int, col_end: int, color: List[int]):
        """Place une ligne de pixel de la même valeur

        Args:
            line (int): ligne concernée
            col_start (int): colonne de départ
            col_end (int): colonne de fin
            color (List[int]): Triplet (R,G,B)
        """
        self.buffer[line,col_start:col_end] = color

    def get(self, x: int, y: int) -> List[int]:
        """Renvoie la valeur du triplet (R,G,B) à la position demandée

        Args:
            x (int): position en pixel en longeur de l'image
            y (int): position en pixel en hauteur de l'image

        Returns:
            List[int]: _description_
        """
        return self.buffer[y,x]

    def draw_image_np(self, img: ImageTk, line_start: int, line_end: int, col_start: int, col_end:int, mask=False):
        """Dessine une image/matrice numpy sur le zbuffer.
        la transparence peut être ignorée avec le paramètre mask=True

        Args:
            img (ImageTk): matrice numpy 
            line_start (int): ligne de départ
            line_end (int): ligne de fin
            col_start (int): colonne de départ
            col_end (int): colonne de fin
            mask (bool, optional): Permet de supprimer la transparence (0,0,0). Defaults to False.
        """
        if not mask:
            self.buffer[line_start:line_end, col_start:col_end] = img
        else:
            mask = np.all(img != [0, 0, 0], axis=2)
            self.buffer[line_start:line_end, col_start:col_end][mask] = img[mask]

    def show(self):
        """Met à jour le conteneur en affichant le zbuffer
        """
        img_pil = Image.fromarray(self.buffer)
        self.img_tk = ImageTk.PhotoImage(img_pil)
        self.container["image"] = self.img_tk

    def clear(self):
        """Nettoie le buffer par sa valeur par défaut
        """
        self.buffer = self.clear_buffer.copy()