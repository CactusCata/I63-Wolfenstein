from PIL import Image, ImageTk
import logic.utils.fileUtils as fileUtils
from math import exp
from typing import List
import numpy as np

import logic.game.option as option
from logic.utils.vec2D import Vec2D

GUN_IMG:Image = None
GUN_IMG_TK:ImageTk = None
GUN_IMG_NP = None

NGUYEN_NORMAL_IMG:Image = None
NGUYEN_NORMAL_IMG_TK:ImageTk = None

NGUYEN_SAVIOR_IMG:Image = None
NGUYEN_SAVIOR_IMG_TK:ImageTk = None

NGUYEN_ZOMBIE_IMG:Image = None
NGUYEN_ZOMBIE_IMG_TK:ImageTk = None

ALIEN_IMG = None

PROFILE_IMG = None
PROFILE_IMG_TK = None

PROFIL_FONT_IMG = None
PROFIL_FONT_IMG_TK = None

ROOF_IMG:List = []
ROOF_IMG_TK:List = []

GROUND_IMG:List = []
GROUND_IMG_TK:List = []

NUMBERS_IMG = []
NUMBERS_IMG_TK = []

#####################
#   Partie Image    #
#####################
def load_image(path:str, resize_dims:Vec2D=None, ratio=-1) -> Image:
    """Charge en mémoire les images

    Args:
        path (str): chemin
        resize_dims (Vec2D, optional): Redimensionnement de l'image. Defaults to None.
        ratio (int, optional): application d'un ratio par rapport à la taille de l'image. Defaults to -1.

    Raises:
        ValueError: _description_

    Returns:
        Image: _description_
    """
    if not fileUtils.file_exist(path):
        raise ValueError(f"The file \"{path}\" do not exist.")
    
    img = Image.open(path)
    if resize_dims != None:
        img = img.resize(resize_dims)
    elif ratio != -1:
        img_dims = img.size
        img = img.resize((int(img_dims[0] * ratio), int(img_dims[1] * ratio)))
    return img

def load_images():
    """Charge toutes les images
    """
    global GUN_IMG, ROOF_IMG, GROUND_IMG, NGUYEN_SAVIOR_IMG, NGUYEN_ZOMBIE_IMG, PROFILE_IMG, NGUYEN_NORMAL_IMG, PROFIL_FONT_IMG, ALIEN_IMG

    GUN_IMG = load_image("../res/img/gun_final.png")
    NGUYEN_ZOMBIE_IMG = load_image("../res/img/nguyen32_zombie.png", resize_dims=Vec2D(80, 80))
    NGUYEN_SAVIOR_IMG = load_image("../res/img/nguyen_the_savior.png", resize_dims=Vec2D(80, 80))
    NGUYEN_NORMAL_IMG = load_image("../res/img/nguyen_normal.png", resize_dims=Vec2D(80, 80))
    PROFILE_IMG = load_image("../res/img/profile_font.png", ratio=0.32)
    ALIEN_IMG = load_image("../res/img/alien_final.png", ratio=3)
    PROFIL_FONT_IMG = load_image("../res/img/profil_font.png", resize_dims=Vec2D(
        option.OPTION.get_drawer_dimensions()[0], option.OPTION.get_info_dimensions()[1]))

    for file_path in fileUtils.get_all_files_in_folder("../res/img/numbers/"):
        number_img = load_image(f"../res/img/numbers/{file_path}", ratio=0.5)
        NUMBERS_IMG.append(number_img)

    for file_path in fileUtils.get_all_files_in_folder("../res/img/ground/"):
        ground_img = load_image(f"../res/img/ground/{file_path}")
        ground_img = ground_img.resize((option.OPTION.get_window_dimensions()[0], option.OPTION.get_window_dimensions()[1] // 2))
        ground_img = ground_img.convert('RGB')
        dark_mask_ground = generate_mask(ground_img.size[1], option.OPTION.get_view_distance())
        dark_mask_ground.reverse()
        ground_img = make_darker(ground_img, dark_mask_ground)
        GROUND_IMG.append(ground_img)


    for file_path in fileUtils.get_all_files_in_folder("../res/img/ground/"):
        roof_img = load_image(f"../res/img/ground/{file_path}")
        roof_img = roof_img.convert('RGB')
        roof_img = roof_img.resize((option.OPTION.get_window_dimensions()[0], option.OPTION.get_window_dimensions()[1] // 2))
        roof_img = rotate_image(roof_img, 180)
        dark_mask_roof = generate_mask(roof_img.size[1], option.OPTION.get_view_distance())
        roof_img = make_darker(roof_img, dark_mask_roof)
        ROOF_IMG.append(roof_img)

#####################
#  Partie Image Tk  #
#####################
def load_image_tk(image:Image) -> ImageTk:
    """Charge une imageTk à partir d'une image

    Args:
        image (Image): image source

    Returns:
        ImageTk: Image chargée
    """
    image_tk = ImageTk.PhotoImage(image)
    #image.close()
    return image_tk

def load_images_tk():
    """Charge les imageTk
    """
    global GUN_IMG_TK, ROOF_IMG_TK, GROUND_IMG_TK, NGUYEN_SAVIOR_IMG_TK, NGUYEN_NORMAL_IMG_TK, NGUYEN_ZOMBIE_IMG_TK, PROFILE_IMG_TK, PROFIL_FONT_IMG_TK, PERCENT_IMG_TK

    GUN_IMG_TK = load_image_tk(GUN_IMG)
    NGUYEN_NORMAL_IMG_TK = load_image_tk(NGUYEN_NORMAL_IMG)
    NGUYEN_SAVIOR_IMG_TK = load_image_tk(NGUYEN_SAVIOR_IMG)
    NGUYEN_ZOMBIE_IMG_TK = load_image_tk(NGUYEN_ZOMBIE_IMG)
    PROFILE_IMG_TK = load_image_tk(PROFILE_IMG)
    PROFIL_FONT_IMG_TK = load_image_tk(PROFIL_FONT_IMG)

    for img in NUMBERS_IMG:
        NUMBERS_IMG_TK.append(load_image_tk(img))

    for img in ROOF_IMG:
        ROOF_IMG_TK.append(load_image_tk(img))

    for img in GROUND_IMG:
        GROUND_IMG_TK.append(load_image_tk(img))

#############
# Partie NP #
#############

def load_images_np():
    """Charge la matrice numpy depuis chaque image
    """
    global GUN_IMG_NP
    
    GUN_IMG_NP = load_image_np(GUN_IMG)

def load_image_np(img:Image):
    """Charge une matrice 

    Args:
        img (ImageTk): Image

    Returns:
        Martice numpy: Matrice numpy sans canal alpha
    """
    return np.array(img)[:,:,:3]



##############
#   Utils    #
##############

def moyenne(img1: Image, img2: Image, coef1: float, coef2: float) -> Image:
    """Renvoie la moyenne de deux images

    Args:
        img1 (Image): Image A
        img2 (Image): Image B
        coef1 (float): coefficent entre 0 et 1
        coef2 (float): coefficient entre coef1 et 1

    Returns:
        Image: Image moyénnée
    """
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Calcul de la moyenne
    arr_avg = coef1 * arr1 + coef2 * arr2

    # Création de l'image moyenne à partir du tableau
    arr_avg = np.clip(arr_avg, 0, 255).astype(np.uint8)
    img_avg = Image.fromarray(arr_avg)
    return img_avg

def generate_mask(height: int, weight: int, limit=20) -> List[float]:
    """Génère un masque de luminosité croissant

    Args:
        height (int): largeur du masque
        weight (int): hauteur du masque
        limit (int, optional): coef a modifier en fonction de la transition. Defaults to 20.

    Returns:
        List[float]: Liste des coefs de luminosité croissante
    """
    dark_coefs = []
    for line in range(height):
        dark_coefs.append(exp(-line * limit / (height * weight)))
    return dark_coefs


def make_darker(img:Image, mask:List[float]) -> Image:
    """Rend une image plus sombre

    Args:
        img (Image): Image source
        mask (List[float]): liste de coefficient

    Returns:
        Image: _description_
    """
    arr = np.array(img).astype(np.float64)
    
    for i in range(arr.shape[0]):
        arr[i,:] *= mask[i]

    arr = np.clip(arr, 0, 255).astype(np.uint8)

    return Image.fromarray(arr)

def rotate_image(img:Image, rot_degree:int) -> Image:
    """Applique une rotation sur une image

    Args:
        img (Image): image source
        rot_degree (int): degree de rotation

    Returns:
        Image: image rotationnée
    """
    return img.rotate(rot_degree)