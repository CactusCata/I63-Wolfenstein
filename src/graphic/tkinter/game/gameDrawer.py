from tkinter import Tk, Label
from math import tan, cos, pi, exp, atan2, sin, atan

from logic.utils.vec2D import Vec2D
import logic.game.game as game
import logic.game.option as option
import logic.utils.mathUtils as mathUtils
import logic.sprite.spriteManager as spriteManager
import logic.utils.mathUtils as mathUtils

from graphic.tkinter.image.zbuffer import ZBuffer

class GameDrawer:

    def __init__(self, root:Tk):
        screen_dims = option.OPTION.get_drawer_dimensions()
        self.container = Label(master=root, width=screen_dims[0], height=screen_dims[1])
        self.container.pack(side="left")
        self.zbuffer = ZBuffer(self.container)

    def draw(self):
        self.create_gun()
        self.create_gun_sight()

        self.zbuffer.clear()
        self.draw_walls()
        self.draw_entities()
        self.zbuffer.show()

    def redraw(self):
        self.zbuffer.clear()
        self.draw_walls()
        self.draw_entities()
        self.zbuffer.show()

    def draw_walls(self):
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
        fov = option.OPTION.get_fov()
        player = game.GAME.get_world().get_player()
        player_rotation = player.get_rotation()
        player_pos = player.get_pos()
        screen_width = option.OPTION.get_drawer_dimensions()[0]
        screen_height = option.OPTION.get_drawer_dimensions()[1]
        virtual_distance = (screen_width / 2) / (tan((fov/2) * pi / 180))

        aliens_pos = []
        for alien in game.GAME.get_world().get_aliens():
            aliens_pos.append(alien.get_pos())

        visibles_aliens = player.get_visibles_entity()
        
        for visible_alien in visibles_aliens:
            pass
    
    def create_gun(self):
        pass
        #self.create_image(option.OPTION.get_window_dimensions()[0] // 2 - 6 ,
        #                  option.OPTION.get_window_dimensions()[1],
        #                  anchor=S,
        #                  image=imageTkManager.GUN_IMG_TK, 
        #                  tags=DEFINITIVE_USE_TAG_2)
        
    def create_gun_sight(self):
        drawer_dims = option.OPTION.get_drawer_dimensions()
        self.zbuffer.set_line(drawer_dims[1] // 2, 
                              drawer_dims[0] // 2 - 5,
                              drawer_dims[0] // 2 + 5,
                              (255, 255, 255))
        self.zbuffer.set_col(drawer_dims[0] // 2,
                             drawer_dims[1] // 2 - 5,
                             drawer_dims[1] // 2 + 5,
                             (255, 255, 255))
        