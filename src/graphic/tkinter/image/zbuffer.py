from tkinter import Label

import numpy as np
import logic.game.option as option

from PIL import Image, ImageTk

class ZBuffer:

    def __init__(self, container:Label):
        self.container = container
        self.img_tk = None
        window_dims = option.OPTION.get_window_dimensions()
        self.clear_buffer = np.zeros([window_dims[1], window_dims[0], 3], dtype=np.uint8)
        self.buffer = self.clear_buffer.copy()

    def set(self, x, y, color):
        self.buffer[y,x] = color

    def set_col(self, col, line_start, line_end, color):
        self.buffer[line_start:line_end,col] = color

    def set_line(self, line, col_start, col_end, color):
        self.buffer[line,col_start:col_end] = color

    def get(self, x, y):
        return self.buffer[y,x]

    def draw_image_np(self, img, line_start, line_end, col_start, col_end, mask=False):
        if not mask:
            self.buffer[line_start:line_end, col_start:col_end] = img
        else:
            mask = np.all(img != [0, 0, 0], axis=2)
            self.buffer[line_start:line_end, col_start:col_end][mask] = img[mask]

    def show(self):
        img_pil = Image.fromarray(self.buffer)
        self.img_tk = ImageTk.PhotoImage(img_pil)
        self.container["image"] = self.img_tk

    def clear(self):
        self.buffer = self.clear_buffer.copy()