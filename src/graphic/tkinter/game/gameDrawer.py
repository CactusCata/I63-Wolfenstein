from tkinter import Canvas
from math import tan, cos, sin, pi, sqrt, exp

from logic.game.game import Game
from logic.world.blockType import BlockType
from logic.utils.vec2D import Vec2D
import logic.game.game as game
import logic.game.option as option
import logic.utils.mathUtils as mathUtils
import logic.sprite.spriteManager as spriteManager


from graphic.utils.tkUtils import ONE_USE_TAG_TUPLE, DEFINITIVE_USE_TAG_TUPLE_0

class GameDrawer:

    def __init__(self, canvas:Canvas):
        self.__canvas = canvas
        

    def draw(self):
        self.draw_background()
        self.draw_game()

    def redraw(self):
        self.draw_game()
        

    def draw_game(self):
        fov = option.OPTION.get_fov()
        player_rotation = game.GAME.get_world().get_player().get_rotation()
        screen_width = option.OPTION.get_window_dimensions()[0]
        screen_height = option.OPTION.get_window_dimensions()[1]
        virtual_distance = (screen_width / 2) / (tan((fov/2) * pi / 180))

        font_image = spriteManager.FONT_IMG
        font_image_height = font_image.get_height()
        
        h = 0.7

        to_print = False

        for col in range(screen_width):
            angle = (col * fov) / screen_width + player_rotation - 1/2 * fov
            distance, percent_wall = self.get_next_wall_distance(angle)
            
            # fix the "lentille effet"
            distance = distance * cos((player_rotation - angle) * pi / 180)
            
            r = h * (virtual_distance / distance)

            wall_column = spriteManager.FONT_IMG.get_vertical_band(percent_wall)

            # Pourcentage de luminosité en fonction de la distance
            luminosity = self.get_luminosity_from_distance(distance)
            wall_column_with_luminosity = []
            for pixel in wall_column:
                wall_column_with_luminosity.append(f"#{int(pixel[0] * luminosity):02x}{int(pixel[1] * luminosity):02x}{int(pixel[2] * luminosity):02x}")

            # print(f" = {}")
            up = int((screen_height - r) // 2)
            down = int((screen_height + r) // 2)
            pixel_img_size = (down - up) / font_image_height
            current_pixel_drawing = 0
            end_pixel_drawing = font_image_height - 1
            if up < 0:
                pixels_not_needed_to_draw = int(-up / pixel_img_size)
                current_pixel_drawing = pixels_not_needed_to_draw
                end_pixel_drawing = end_pixel_drawing - pixels_not_needed_to_draw

            current_color = wall_column_with_luminosity[current_pixel_drawing]
            start_drawing = max(up, 0)
            end_drawing = (current_pixel_drawing + 1) * pixel_img_size + up

            while current_pixel_drawing < end_pixel_drawing:
                if current_color == wall_column_with_luminosity[current_pixel_drawing + 1]:
                    end_drawing += pixel_img_size
                else:
                    self.__canvas.create_line(col, 
                                              start_drawing, 
                                              col,
                                              end_drawing, 
                                              tags=ONE_USE_TAG_TUPLE,
                                              fill=current_color
                                              )
                    current_color = wall_column_with_luminosity[current_pixel_drawing + 1]
                    start_drawing = end_drawing
                    end_drawing = start_drawing + pixel_img_size
                current_pixel_drawing += 1


            self.__canvas.create_line(col, 
                                        start_drawing, 
                                        col,
                                        end_drawing, 
                                        tags=ONE_USE_TAG_TUPLE,
                                        fill=current_color
                                        )
        

    
    def get_luminosity_from_distance(self, distance):
        return exp(-distance)
        #return "#" + str(f"{res:02X}") * 3
    
    def get_next_wall_distance(self, alpha):
        alpha %= 360
        tan_alpha = tan(alpha * pi / 180)
        world_matrix = game.GAME.get_world().world_matrix
        player_pos = game.GAME.get_world().get_player().get_pos()
        x = player_pos[0]
        y = player_pos[1]

        ivx = 0
        ivy = 0
        ihx = 0
        ihy = 0
        coef_v = 1
        coef_h = 1
        magic_v = 0
        magic_h = 0

        if alpha < 90:
            ivx = int(x) + 1
            ivy = y + abs(x - ivx) * tan_alpha
            ihy = int(y) + 1
            ihx = x + abs(y - ihy) / tan_alpha
        elif alpha < 180:
            ivx = int(x)
            ivy = y + abs(x - ivx) * tan_alpha * -1
            ihy = int(y) + 1
            ihx = x + abs(y - ihy) / tan_alpha
            coef_v = -1
            magic_v = -1
        elif alpha < 270:
            ivx = int(x)
            ivy = y + abs(x - ivx) * tan_alpha * -1
            ihy = int(y)
            ihx = x + abs(y - ihy) / tan_alpha * -1
            coef_v = -1
            magic_v = -1
            coef_h = -1
            magic_h = -1
        else:
            ivx = int(x) + 1
            ivy = y + abs(x - ivx) * tan_alpha
            ihy = int(y)
            ihx = x + abs(y - ihy) / tan_alpha * -1
            coef_h = -1
            magic_h = -1

        div = mathUtils.euclidian_distance(x, y, ivx, ivy)
        dih = mathUtils.euclidian_distance(x, y, ihx, ihy)

        to_add_vx = coef_v
        to_add_vy = coef_v * tan_alpha
        to_add_hx = coef_h / tan_alpha
        to_add_hy = coef_h

        distance_to_add_v = mathUtils.euclidian_distance(ivx, ivy, ivx + to_add_vx, ivy + to_add_vy)
        distance_to_add_h = mathUtils.euclidian_distance(ihx, ihy, ihx + to_add_hx, ihy + to_add_hy)


        
        while True:
            if div < dih: # On gère l'intersection verticale
                if world_matrix[int(ivy)][int(ivx + magic_v)] == BlockType.WALL:
                    return div, (ivy % 1)
                ivx += to_add_vx
                ivy += to_add_vy
                div += distance_to_add_v
                #div = mathUtils.euclidian_distance(x, y, ivx, ivy)
            else: # On gère l'intersection horizontale
                if world_matrix[int(ihy + magic_h)][int(ihx)] == BlockType.WALL:
                    return dih, (ihx % 1)
                ihx += to_add_hx
                ihy += to_add_hy
                dih += distance_to_add_h
                #dih = mathUtils.euclidian_distance(x, y, ihx, ihy)

    def draw_ground(self, band_amount=50):
        window_dimensions = option.OPTION.get_window_dimensions()

        hight_to_remove = window_dimensions[1] / (2 * (band_amount + 1))
        current_hight = window_dimensions[1] - 1
        x = 2
        while current_hight >= window_dimensions[1] // 2:
            red = exp(-x/25) * 255
            self.__canvas.create_rectangle(0, 
                                           current_hight, 
                                           window_dimensions[0], 
                                           current_hight - hight_to_remove, 
                                           fill=f"#{int(red):02X}0000",
                                           outline=f"#{int(red):02X}0000",
                                           tags=DEFINITIVE_USE_TAG_TUPLE_0)
            current_hight -= hight_to_remove
            x *= 1.1

    def draw_roof(self, band_amount=50):
        window_dimensions = option.OPTION.get_window_dimensions()

        hight_to_add = window_dimensions[1] / (2 * (band_amount + 1))
        current_hight = 0
        x = 2
        while current_hight <= window_dimensions[1] // 2:
            red = exp(-x/25) * 255
            self.__canvas.create_rectangle(0, 
                                           current_hight, 
                                           window_dimensions[0], 
                                           current_hight + hight_to_add, 
                                           fill=f"#{int(red):02X}0000",
                                           outline=f"#{int(red):02X}0000",
                                           tags=DEFINITIVE_USE_TAG_TUPLE_0)
            current_hight += hight_to_add
            x *= 1.1

    def draw_background(self):
        self.draw_ground()
        self.draw_roof()

        #self.__canvas.create_rectangle(0, 0, window_dimensions[0], window_dimensions[1] // 2, fill="blue")
        #self.__canvas.create_rectangle(0, window_dimensions[1] // 2, window_dimensions[0], window_dimensions[1], fill="gray")


        