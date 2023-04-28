from typing import List, Tuple
import os
from PIL import Image

def file_exist(path):
    """
    Renvoie True si le fichier existe
    Sinon renvoie False
    """
    return os.path.exists(path)

def read_img_data(image:Image) -> List[List[Tuple]]:
    """
    Renvoie une liste (correspondant aux colonnes de l'image)
    de liste (correspondant à la ligne de la colonne courante)
    """
    brut_data = image.getdata()
    width, height = image.size

    data:List[List[Tuple]] = []
    for i in range(height):
        data.append([])

    for col in range(width):
        for line in range(height):
            data[col].append(brut_data[line * width + col])

    return data    