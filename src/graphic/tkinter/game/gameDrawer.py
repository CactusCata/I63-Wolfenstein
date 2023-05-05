from tkinter import Canvas
from math import tan, cos, sin, pi, sqrt, exp, acos, atan2

from logic.game.game import Game
from logic.world.blockType import BlockType
from logic.utils.vec2D import Vec2D
import logic.game.game as game
import logic.game.option as option
import logic.utils.mathUtils as mathUtils
import logic.sprite.spriteManager as spriteManager
import logic.utils.mathUtils as mathUtils


from graphic.utils.tkUtils import ONE_USE_TAG_TUPLE, DEFINITIVE_USE_TAG_TUPLE_0

class GameDrawer:

    def __init__(self, canvas:Canvas):
        self.__canvas = canvas
        

    def draw(self):
        self.draw_game()

    def redraw(self):
        self.draw_game()

    def draw_walls(self):
        fov = option.OPTION.get_fov()
        player = game.GAME.get_world().get_player()
        player_rotation = player.get_rotation()
        player_pos = player.get_pos()
        screen_width = option.OPTION.get_window_dimensions()[0]
        screen_height = option.OPTION.get_window_dimensions()[1]
        virtual_distance = (screen_width / 2) / (tan((fov/2) * pi / 180))

        # Texture à dessiner sur les murs
        font_image = spriteManager.FONT_IMG
        font_image_height = font_image.get_height()

        view_distance = option.OPTION.get_view_distance()
        
        # Hauteur des murs
        h = 1.0

        #last_n = len(self.__canvas.find("all"))
        for col in range(screen_width):
            #n = len(self.__canvas.find("all"))
            #print(f"Current items amount: {n - last_n}")
            #last_n = n
            # Angle du rayon par rapport au joueur
            angle = (col * fov) / screen_width + player_rotation - 1/2 * fov


            distance, percent_wall = self.get_next_wall_distance(player_pos, angle)
            
            # fix the "lentille effet"
            distance = distance * cos((player_rotation - angle) * pi / 180)
            
            r = h * (virtual_distance / distance)

            wall_column = spriteManager.FONT_IMG.get_vertical_band(percent_wall)
            #print(f"wall col = {int(16 * percent_wall)}")

            # Pourcentage de luminosité en fonction de la distance
            luminosity = max(option.OPTION.get_min_luminosity(), self.get_luminosity_from_distance(distance / (0.4 * view_distance)))
            wall_column_with_luminosity = []
            for pixel in wall_column:
                wall_column_with_luminosity.append(f"#{int(pixel[0] * luminosity):02x}{int(pixel[1] * luminosity):02x}{int(pixel[2] * luminosity):02x}")

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
                    self.create_vertical_line(col, 
                                      start_drawing, 
                                      end_drawing,
                                      ONE_USE_TAG_TUPLE,
                                      current_color
                                      )
                    current_color = wall_column_with_luminosity[current_pixel_drawing + 1]
                    start_drawing = end_drawing
                    end_drawing = start_drawing + pixel_img_size
                current_pixel_drawing += 1


            self.create_vertical_line(col, 
                                      start_drawing, 
                                      end_drawing + 2,
                                      ONE_USE_TAG_TUPLE,
                                      current_color
                                      )
        
    def create_vertical_line(self, x, start_y, end_y, tags, color):
        self.__canvas.create_line(x, 
                                  start_y, 
                                  x,
                                  end_y, 
                                  tags=tags,
                                  fill=color
                                  )

    def draw_entities(self):
        fov = option.OPTION.get_fov()
        player = game.GAME.get_world().get_player()
        player_rotation = player.get_rotation()
        player_pos = player.get_pos()
        screen_width = option.OPTION.get_window_dimensions()[0]
        screen_height = option.OPTION.get_window_dimensions()[1]
        virtual_distance = (screen_width / 2) / (tan((fov/2) * pi / 180))

        aliens_pos = []
        for alien in game.GAME.get_world().get_aliens():
            aliens_pos.append(alien.get_pos())

        visibles_aliens = self.get_visibles_entity(player_pos, 
                                                     player_rotation * pi / 180, 
                                                     fov)
        
        for visible_alien in visibles_aliens:
            pass

        

    def draw_game(self):
        self.draw_walls()
        self.draw_entities()

    
    def get_luminosity_from_distance(self, distance):
        return exp(-distance)
        #return "#" + str(f"{res:02X}") * 3
    
    def get_next_wall_distance(self, player_pos:Vec2D, alpha:float):
        """
        Renvoie la distance entre le joueur et le prochain
        mur touché avec l'angle alpha
        """
        alpha %= 360
        tan_alpha = tan(alpha * pi / 180)
        world_matrix = game.GAME.get_world().world_matrix
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
            else: # On gère l'intersection horizontale
                if world_matrix[int(ihy + magic_h)][int(ihx)] == BlockType.WALL:
                    return dih, (ihx % 1)
                ihx += to_add_hx
                ihy += to_add_hy
                dih += distance_to_add_h

    def entity_is_in_fov(self, mob_pos, player_pos, player_rot, fov):
        u = (mob_pos[0] - player_pos[0], mob_pos[1] - player_pos[1])
        v = (cos(player_rot), sin(player_rot))
        norme_u = mathUtils.norme_2(u)
        prod_scal_uv = mathUtils.prod_scalaire_2(u, v)
        angle = acos(prod_scal_uv / norme_u)

        return angle * 180 / pi < fov // 2, angle
    
    def is_wall_between_player_and_alien(self, player_pos:Vec2D, alien_pos:Vec2D):
        delta_xy = alien_pos - player_pos

        # Calcul de l'angle en radians
        angle_rad = atan2(delta_xy[1], delta_xy[0])

        # Conversion en degrés
        alpha = angle_rad * 180 / pi
        distance_to_next_wall,_ = self.get_next_wall_distance(player_pos, alpha)
        distance_to_alien = delta_xy.distance(player_pos)

        return distance_to_alien > distance_to_next_wall


    def get_visibles_entity(self, player_pos, player_rot, fov):
        visibles_entities = []
        for alien in game.GAME.get_world().get_aliens():
            if self.entity_is_in_fov(alien.get_pos(), player_pos, player_rot, fov):
                if not self.is_wall_between_player_and_alien(player_pos, alien.get_pos()):
                    visibles_entities.append(alien)
        return visibles_entities