from PIL import Image
from typing import List, Tuple

import logic.utils.fileUtils as fileUtils

class Sprite:

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
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height