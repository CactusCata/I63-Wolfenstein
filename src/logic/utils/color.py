class Color:

    def __init__(self, r:int, g:int, b:int):
        self.colors = (r, g, b)

    def __getitem__(self, index:int):
        return self.colors[index]


def health_to_color(health_percent:float):
    """
    healthPercent: nombre E [0;100]
    Renvoie le code hexadécimal de la couleur correspondant
    au pourcentage de point de vie
    """
    r = min(255, 255 - int((health_percent - 50) * (255 / 50)))
    g = min(255, int(health_percent * (255 / 50)))
    b = 0