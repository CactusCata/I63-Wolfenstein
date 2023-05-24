from typing import List, Tuple
import os
from PIL import Image

def file_exist(path:str) -> bool:
    """Informe sur l'existance d'un fichier

    Args:
        path (str): Chemin du fichier

    Returns:
        bool: True si le fichier existe, False sinon
    """
    return os.path.exists(path)

def read_img_data(image:Image) -> List[List[Tuple]]:
    """Renvoie une liste (correspondant aux colonnes de l'image)
    de liste (correspondant à la ligne de la colonne courante)

    Args:
        image (Image): Image a analyser

    Returns:
        List[List[Tuple]]: Matrice colonne x ligne de l'image avec des valeurs RGB
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

def get_all_files_in_folder(path:str) -> List[str]:
    """Renvoie la liste des noms de fichier contenu dans un dossier

    Args:
        path (str): Chemin

    Returns:
        List[str]: Liste des noms de fichier contenu dans un dossier
    """
    return os.listdir(path)