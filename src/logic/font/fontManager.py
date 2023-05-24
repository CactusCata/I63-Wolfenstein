from PIL import Image, ImageTk
import logic.utils.fileUtils as fileUtils
import numpy as np
from tkinter import Canvas, NW
from logic.utils.vec2D import Vec2D
from typing import List
from graphic.tkinter.utils.tkUtils import DEFINITIVE_USE_TAG_TUPLE_2

"""
Permet de générer du texte depuis une table de symbole
avec une certaine police d'écriture
"""

letters = ["!","\"","#","$","%","&","'","(",")","*","+",",","-",
           ".","/","0","1","2","3","4","5","6","7","8","9",":",
           ";","<","=",">","?","@","A","B","C","D","E","F","G",
           "H","I","J","K","L","M","N","O","P","Q","R","S","T",
           "U","V","W","X","Y","Z","[","\\","]","^","_","`","a",
           "b","c","d","e","f","g","h","i","j","k","l","m","n",
           "o","p","q","r","s","t","u","v","w","x","y","z"]

letters_px = None

char_translation = []
char_translation_tk = []

def load_font(path:str, ratio=1):
    """Charge la sprite sheet de symbole depuis un fichier

    Args:
        path (str): chemin du fichier
        ratio (int, optional): Ratio par rapport à la taille des caractères. Defaults to 1.

    Raises:
        ValueError: Si le fichier n'existe pas
        ValueError: Si la taille des caractères n'a pas été calculée avant
    """
    if not fileUtils.file_exist(path):
        raise ValueError(f"The file named \"{path}\" do not exist.")
    if letters_px is None:
        raise ValueError(f"You need to init seprators first !")
    
    font_img = Image.open(path)
    font_img_np_array = np.array(font_img)

    for start_px, end_px in letters_px:
        char_image_selection = font_img_np_array[1:,start_px:end_px+1,:]
        char_image = Image.fromarray(char_image_selection)
        char_image_dims = char_image.size
        char_image = char_image.resize(
            (int(ratio * char_image_dims[0]), 
             int(ratio * char_image_dims[1]))
        )
        char_translation.append(char_image)

def load_font_tk():
    """Charge les images de symbole
    """
    for img in char_translation:
        image_tk = ImageTk.PhotoImage(img)
        img.close()
        char_translation_tk.append(image_tk)

def init_separators(path:str):
    """Calcul la taille des symboles en pixel

    Args:
        path (str): Chemin du fichier

    Raises:
        ValueError: Si le fichier n'exitste pas
    """
    if not fileUtils.file_exist(path):
        raise ValueError(f"The file named \"{path}\" do not exist.")
    
    global letters_px
    
    font_img = Image.open(path)
    font_img_data = list(font_img.getdata())
    font_img_dims = font_img.size

    line_data = font_img_data[:font_img_dims[0]]
    start = 0
    letters_px = []
    for c in range(1, font_img_dims[0]):
        if line_data[c] == (47, 99, 35, 255):
            letters_px.append((start, c - 1))
            start = c


def translate(text:str):
    """Renvoie, pour chaque caractère du texte, une image correspondant
    au symbole mais dans la police d'écriture prévu.

    Args:
        text (str): texte à traduire

    Returns:
        List[ImageTk]: Liste des symboles
    """
    char_image_tk:List = []
    for c in text:
        if c in letters:
            char_image_tk.append(char_translation_tk[letters.index(c)])
        elif c == ' ':
            char_image_tk.append(None)
        else:
            char_image_tk.append(char_translation_tk[letters.index('?')])
    return char_image_tk

def write_text(canvas:Canvas, text:str, pos_nw:Vec2D, char_space_px:int) -> List[int]:
    """Ecrit un texte avec la bonne police d'écriture

    Args:
        canvas (Canvas): canvas de dessin
        text (str): texte à traduire
        pos_nw (Vec2D): position de départ d'écriture des symboles
        char_space_px (int): espace en pixel entre les symboles

    Returns:
        List[int]: Liste des identifiants de chaque image crée
    """
    images = translate(text)

    imgs_ids = []
    start_x, start_y = pos_nw
    for img in images:
        if img == None:
            start_x += 4 * char_space_px
        else:
            img_id = canvas.create_image(start_x,
                                        start_y,
                                        image=img,
                                        anchor=NW,
                                        tags=DEFINITIVE_USE_TAG_TUPLE_2)
            imgs_ids.append(img_id)
            start_x += img.width()
        start_x += char_space_px
    return imgs_ids