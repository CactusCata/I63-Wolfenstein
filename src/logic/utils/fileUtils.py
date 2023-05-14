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
    #print("Reading image 1...")
    brut_data = image.getdata()
    #print(list(brut_data))
    #print("-"*30)
    width, height = image.size

    data:List[List[Tuple]] = []
    for i in range(height):
        data.append([])

    for col in range(width):
        for line in range(height):
            data[col].append(brut_data[line * width + col][:3])

    return data    

def get_all_files_in_folder(path:str):
    return os.listdir(path)