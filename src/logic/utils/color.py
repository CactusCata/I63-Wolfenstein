class Color:

    def __init__(self, r:int, g:int, b:int):
        self.colors = (r, g, b)

    def __getitem__(self, index:int):
        return self.colors[index]
