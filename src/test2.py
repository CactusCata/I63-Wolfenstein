from tkinter import Tk, Label, Canvas
import numpy as np
from PIL import ImageTk, Image
from random import randint

window_width = 809
window_height = 500

img_tk = None

def draw_np_array(label:Label, np_array):
    global img_tk
    img_pil = Image.fromarray(np_array)
    img_tk = ImageTk.PhotoImage(img_pil)
    label["image"] = img_tk

def draw_random(root:Tk, label:Label, np_array):
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    for i in range(window_height):
            np_array[i,5] = color

    draw_np_array(label, np_array)
    root.after(1, lambda: draw_random(root, label, np_array))


if __name__ == "__main__":

    root = Tk()
    root.geometry(f"{window_width}x{window_height}")

    label = Label(root)
    label.place(x=0, y=0)

    #canvas = Canvas(root)
    #canvas.place(x=0, y=0)

    np_array = np.zeros([window_height, window_width, 3], dtype=np.uint8)
    np_array[30:50] = (255, 0, 0)

    draw_random(root, label, np_array)
    
    
    


    root.mainloop()



"""
algo du peintre: on dessine tout puis on dessine le sprite d'alien
si on ne bouge pas et que l'alien bouge, on lift le dessin de mur et on redessine l'alien
si on bouge, on recalcul tout
"""