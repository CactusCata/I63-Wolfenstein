import os

def file_exist(path):
    """
    Renvoie True si le fichier existe
    Sinon renvoie False
    """
    return os.path.exists(path)
