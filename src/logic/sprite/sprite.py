from PIL import Image
from typing import List, Tuple

import logic.utils.fileUtils as fileUtils

class Sprite:
    """
    Objet utilisé pour le dessin en raycasting
    """

    def __init__(self, path:str) -> None:
        if not fileUtils.file_exist(path):
            raise ValueError(f"The file \"{path}\" do not exist")
        
        image = Image.open(path)
        self.width, self.height = image.size
        self.pixels = fileUtils.read_img_data(image)
        image.close()

    def get_vertical_band(self, band_percentage_needed:float) -> List[Tuple[int]]:
        """
        Renvoie la bande verticale de l'image selon un pourcentage
        """
        return self.pixels[int(band_percentage_needed * self.width)]
    
    def get(self, percent_x: float, percent_y: float) -> Tuple[int]:
        """Renvoie le triplet (R,G,B) d'une position de l'image

        Args:
            percent_x (float): ratio de l'emplacement visé en X
            percent_y (float): ratio de l'emplacement visé en X

        Returns:
            Tuple[int]: Triplet (R,G,B) d'une position de l'image
        """
        return self.pixels[int(percent_y * self.width)][int(percent_x * self.height)]
    
    def get_width(self) -> int:
        """Renvoie la largeur de l'image en pixel

        Returns:
            int: Largeur de l'image en pixel
        """
        return self.width
    
    def get_height(self) -> int:
        """Renvoie la hauteur de l'image en pixel

        Returns:
            int: Hauteur de l'image en pixel
        """
        return self.height