from tkinter import Tk, Label
from math import tan, cos, pi, exp, atan2, sin, atan
import numpy as np

from time import time
from logic.utils.vec2D import Vec2D
import logic.game.game as game
import logic.game.option as option
import logic.utils.mathUtils as mathUtils
import logic.sprite.spriteManager as spriteManager
import logic.utils.mathUtils as mathUtils
import logic.imagetk.imageTkManager as imageTkManager

from graphic.tkinter.image.zbuffer import ZBuffer

class GameDrawer:
    """Classe du raycastring (dessin du jeu Tkinter)
    """

    def __init__(self, root:Tk):
        """Constructeur

        Args:
            root (Tk): Fenetre tkinter
        """
        screen_dims = option.OPTION.get_drawer_dimensions()
        self.container = Label(master=root, width=screen_dims[0], height=screen_dims[1])
        self.container.pack(side="left")
        self.zbuffer = ZBuffer(self.container)

        self.fps_counter = 0
        self.fps_current_sec = 0

    def draw(self):
        """Dessine tous les éléments à l'écran
        """
        self.zbuffer.clear()
        self.draw_walls()
        self.draw_entities()
        self.draw_gun()
        self.draw_gun_sight()
        self.zbuffer.show()

        self.check_fps()

    def redraw(self):
        """Redessine tous les éléments à l'écran
        """
        self.zbuffer.clear()
        self.draw_walls()
        self.draw_entities()
        self.draw_gun()
        self.draw_gun_sight()
        self.zbuffer.show()

        self.check_fps()

    def check_fps(self):
        """Affiche les fps
        """
        if int(time()) == self.fps_current_sec:
            self.fps_counter += 1
        else:
            self.fps_current_sec = int(time())
            print(f"Tk fps: {self.fps_counter}")
            self.fps_counter = 1

    def draw_walls(self):
        """Dessine les murs avec l'algo DDA
        """
        fov = option.OPTION.get_fov()
        world = game.GAME.get_world()
        player = world.get_player()
        player_rotation = player.get_rotation()
        player_pos = player.get_pos()
        screen_width = option.OPTION.get_drawer_dimensions()[0]
        screen_height = option.OPTION.get_drawer_dimensions()[1]
        virtual_distance = (screen_width / 2) / (tan((fov/2) * pi / 180))

        # Texture à dessiner sur les murs
        font_image = spriteManager.FONT_IMG
        font_image_height = font_image.get_height()

        view_distance = option.OPTION.get_view_distance()
        
        # Hauteur des murs
        h = 1.0

        for col in range(screen_width):
            # Angle du rayon par rapport au joueur
            angle = (col * fov) / screen_width + player_rotation - 1/2 * fov


            distance, percent_wall, hit_wall_coords = world.get_next_wall_distance(player_pos, angle)
            
            # fix the "lentille effet"
            distance = distance * cos((player_rotation - angle) * pi / 180)
            
            r = h * (virtual_distance / distance)

            wall_column = spriteManager.FONT_IMG.get_vertical_band(percent_wall)

            # Pourcentage de luminosité en fonction de la distance
            luminosity = exp(-distance / (0.4 * view_distance))
            luminosity = max(option.OPTION.get_min_luminosity(), luminosity)
            wall_column_with_luminosity = []
            for pixel in wall_column:
                wall_column_with_luminosity.append((int(pixel[0] * luminosity), int(pixel[1] * luminosity), int(pixel[2] * luminosity)))

            # Dessin de la ligne de `start_drawing` à `final_drawing`
            start_drawing = int((screen_height - r) // 2)
            final_drawing = int((screen_height + r) // 2)
            # Taille verticale d'un pixel de l'image sur l'écran
            pixel_img_size = (final_drawing - start_drawing) / font_image_height

            # Pixels de debut et de fin à dessiner à l'écran
            current_pixel_drawing = 0
            end_pixel_drawing = font_image_height - 1
            if start_drawing < 0:
                pixels_not_needed_to_draw = int(-start_drawing / pixel_img_size)
                current_pixel_drawing = pixels_not_needed_to_draw
                end_pixel_drawing = end_pixel_drawing - pixels_not_needed_to_draw

            current_color = wall_column_with_luminosity[current_pixel_drawing]
            end_drawing = (current_pixel_drawing + 1) * pixel_img_size + start_drawing
            start_drawing = max(start_drawing, 0)

            while current_pixel_drawing < end_pixel_drawing:
                if current_color == wall_column_with_luminosity[current_pixel_drawing + 1]:
                    end_drawing += pixel_img_size
                else:
                    #print(f"The color is not the same ! {current_color} != {wall_column_with_luminosity[current_pixel_drawing + 1]}")
                    self.zbuffer.set_col(int(col), int(start_drawing), int(end_drawing), current_color)
                    current_color = wall_column_with_luminosity[current_pixel_drawing + 1]
                    start_drawing = end_drawing
                    end_drawing = start_drawing + pixel_img_size
                current_pixel_drawing += 1

            self.zbuffer.set_col(int(col), int(start_drawing), int(end_drawing) + 2, current_color)

            """
            # Draw ground
            if end_drawing < screen_height:
                
                #print('-' * 30)
                #print(distance)
                alpha = atan((r//2) / virtual_distance)
                beta = atan((screen_height//2) / virtual_distance)
                gamma = (beta - alpha) / ((screen_height - r) // 2)
                #print(alpha * 180 / pi, beta * 180 / pi, gamma * 180 / pi)
                end_drawing = int(end_drawing)
                i = 0
                # Draw ground
                for line in range(end_drawing, screen_height):
                    op = tan(((pi/2) - (gamma * i + alpha))) * 0.5
                    #print(op)
                    ratio_distance = op / distance
                    pos = (ratio_distance * player_pos[0] + (1 - ratio_distance) * hit_wall_coords[0],
                           ratio_distance * player_pos[1] + (1 - ratio_distance) * hit_wall_coords[1])

                    #print(f"block target is {pos}")
                    color = spriteManager.ALIEN_IMAGE.get(pos[0] % 1, pos[1] % 1)
                    self.zbuffer.set(col, line, color)
                    i += 1

                #if (screen_height - end_drawing > 20):
                #    exit()
            """



            
            

    def draw_entities(self):
        """Dessine les entités
        """
        player = game.GAME.get_world().get_player()
        player_pos = player.get_pos()
        screen_width = option.OPTION.get_drawer_dimensions()[0]
        screen_height = option.OPTION.get_drawer_dimensions()[1]
        fov = option.OPTION.get_fov()


        visibles_aliens = player.get_visibles_entity()
        img_dims = imageTkManager.ALIEN_IMG.size

        player.reset_alien_aimed()
        for visible_alien, alpha in visibles_aliens:
            alien_pos = visible_alien.get_pos()
            distance = mathUtils.euclidian_distance(player_pos[0], player_pos[1], alien_pos[0], alien_pos[1])
            
            img = imageTkManager.ALIEN_IMG.resize((int(img_dims[0] / distance), int(img_dims[1] / distance)))
            new_img_dims = img.size
            img_np = np.array(img)[:,:,:3]
            start_line = option.OPTION.get_drawer_dimensions()[1] // 2 - new_img_dims[1] // 2
            end_line = start_line + new_img_dims[1]
            start_col = int(((alpha + fov // 2) / fov) * screen_width - new_img_dims[0])
            end_col = int(start_col + new_img_dims[0])
            
            if start_line < 0:
                to_remove_start_line = -start_line
                start_line = 0
                img_np = img_np[to_remove_start_line:,:]

            if end_line >= option.OPTION.get_drawer_dimensions()[1]:
                to_remove_end_line = end_line - option.OPTION.get_drawer_dimensions()[1] + 1
                end_line = option.OPTION.get_drawer_dimensions()[1] - 1
                img_np = img_np[:-to_remove_end_line,:]
                
            if start_col < 0:
                to_remove_col = -start_col
                start_col = 0
                img_np = img_np[:,to_remove_col:]

            if end_col >= option.OPTION.get_drawer_dimensions()[0]:
                to_remove_col = option.OPTION.get_drawer_dimensions()[0] - end_col + 1
                end_col = option.OPTION.get_drawer_dimensions()[0] - 1
                img_np = img_np[:,:end_col + 1]

            middle_column = option.OPTION.drawer_dimensions[0] // 2

            if start_col <= middle_column <= end_col:
                player.set_alien_aimed(visible_alien)

            
            self.zbuffer.draw_image_np(img_np, start_line, end_line, start_col, end_col, True)
    
    def draw_gun(self):
        """Dessine le gun
        """
        self.zbuffer.draw_image_np(imageTkManager.GUN_IMG_NP,
                                    option.OPTION.get_drawer_dimensions()[1] - 127,
                                    option.OPTION.get_drawer_dimensions()[1], 
                                    option.OPTION.get_drawer_dimensions()[0] // 2 - 80,
                                    option.OPTION.get_drawer_dimensions()[0] // 2 + 86,
                                    mask=True)
        
    def draw_gun_sight(self):
        """Dessine le viseur
        """
        drawer_dims = option.OPTION.get_drawer_dimensions()
        self.zbuffer.set_line(drawer_dims[1] // 2, 
                              drawer_dims[0] // 2 - 5,
                              drawer_dims[0] // 2 + 5,
                              (255, 255, 255))
        self.zbuffer.set_col(drawer_dims[0] // 2,
                             drawer_dims[1] // 2 - 5,
                             drawer_dims[1] // 2 + 5,
                             (255, 255, 255))
        