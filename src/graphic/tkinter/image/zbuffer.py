from tkinter import Label

import numpy as np
import logic.game.option as option

from PIL import Image, ImageTk

class ZBuffer:

    def __init__(self, container:Label):
        self.container = container
        self.img_tk = None
        window_dims = option.OPTION.get_window_dimensions()
        self.buffer = np.zeros([window_dims[1], window_dims[0], 3], dtype=np.uint8)

    def set(self, x, y, color):
        self.buffer[y,x] = color

    def set_col(self, col, line_start, line_end, color):
        self.buffer[line_start:line_end,col] = color

    def set_line(self, line, col_start, col_end, color):
        self.buffer[line,col_start:col_end] = color

    def show(self):
        img_pil = Image.fromarray(self.buffer)
        self.img_tk = ImageTk.PhotoImage(img_pil)
        self.container["image"] = self.img_tk

    def clear(self):
        window_dims = option.OPTION.get_window_dimensions()
        self.buffer = np.zeros([window_dims[1], window_dims[0], 3], dtype=np.uint8)
        self.container["image"] = None