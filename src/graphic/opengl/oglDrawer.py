from __future__ import annotations

from math import pi, tan, sqrt

import numpy
from OpenGL.GL import *
from PIL import Image
from pyopengltk import OpenGLFrame

import logic.game.game as game
from logic.world.blockType import BlockType
from logic.world.world import WORLD_DIM_X, WORLD_DIM_Y

GOD_MODE = False
"""
Affiche une vue du dessus de la map.
"""

TEX_AHMED = 1
TEX_NETHERRACK = 2


class OGLDrawer(OpenGLFrame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.player = game.GAME.get_world().get_player()

    def initgl(self):
        """
        Called when frame goes onto the screen or is resized.

        See: BaseOpenGLFrame#tkMap()
             BaseOpenGLFrame#tkResize()
        """

        # Configuration initiale d'OpenGL

        glEnable(GL_DEPTH_TEST)

        if not GOD_MODE or True:
            glEnable(GL_CULL_FACE)

        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 1, 1, 1))

        # 1/(kc + kl.d + kq.d²)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, .01)

        glEnable(GL_TEXTURE_2D)

        # Textures

        load_tex(TEX_AHMED, "ahmed.png", 128)
        load_tex(TEX_NETHERRACK, "netherrack.png", 16)

        # Matériaux
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (1, 1, 1, 1))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (1, 1, 1, 1))
        glMaterialf(GL_FRONT, GL_SHININESS, 0)

        # Matrice de projection

        glViewport(0, 0, self.width, self.height)
        glClearColor(0.0, 0.0, 0.0, 0.0)    

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        fov = 60 * pi/180
        z_near = .1
        z_far = sqrt((WORLD_DIM_X * WORLD_DIM_X) + (WORLD_DIM_Y * WORLD_DIM_Y))

        r = z_near * tan(fov / 2)
        t = (3 * r) / 4

        glFrustum(-r, r, -t, t, z_near, z_far)

        # gluPerspective(60, 4/3, z_near, z_far)

        glMatrixMode(GL_MODELVIEW)

    def redraw(self):
        """
        Render a single frame.
        """

        # Remarque:
        #   Mon +x est son -x, d'où les magouilles dans la composante x.

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        # Caméra
        if not GOD_MODE:
            glRotatef(self.player.rotation + 90, 0, 1, 0)
            glTranslatef(-(self.player.x - WORLD_DIM_X / 2), 0, -(self.player.y - WORLD_DIM_Y / 2))
        else:
            glRotatef(-90, 1, 0, 0)
            glRotatef(-self.player.rotation - 90, 0, 1, 0)
            glTranslatef(-(self.player.x - WORLD_DIM_X / 2), 10, -(self.player.y - WORLD_DIM_Y / 2))

        # Lumière
        glLightfv(GL_LIGHT0, GL_POSITION, (self.player.x - WORLD_DIM_X / 2, 0, self.player.y - WORLD_DIM_Y / 2, 1))

        # Sol & plafond
        glBindTexture(GL_TEXTURE_2D, TEX_NETHERRACK)
        glMaterialfv(GL_FRONT, GL_AMBIENT, (1, 1, 1, 1))
        draw_flooring()
        draw_ceiling()

        # Murs

        glBindTexture(GL_TEXTURE_2D, TEX_AHMED)
        glMaterialfv(GL_FRONT, GL_AMBIENT, (.5, .5, .5, 1))
        glColor4f(1, 1, 1, 1)

        for x in range(WORLD_DIM_X):
            for y in range(WORLD_DIM_Y):
                if self.player.world.world_matrix[y][x] == BlockType.WALL:
                    glPushMatrix()
                    glTranslatef(x - WORLD_DIM_X / 2, 0, y - WORLD_DIM_Y / 2)
                    draw_wall()
                    glPopMatrix()
        
        glPopMatrix()


def load_tex(id, filename, size):
    """
    Charge une texture.

    :param id: le nom de la texture, cf. `glGenTextures()`.
    :param filename: le nom du fichier
    :param size: la longueur du côté de l'image
    """

    _bytes = numpy.array(Image.open(f"../res/img/{filename}").getdata(), numpy.uint8)

    glBindTexture(GL_TEXTURE_2D, id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB8, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, _bytes)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)


def draw_wall():
    #
    #  v1 --- v3    y = 1
    #   |     |
    #   |     |
    #  v0 --- v2    y = 0
    #
    #  x +/- 0.5
    #
    #
    #     * --- *
    #    /|    /|
    #   / |   / |
    #  * --- *  *
    #  |     | /
    #  |     |/
    #  * --- *
    #
    #  pas de plafond ni de sol
    #

    glBegin(GL_QUAD_STRIP)

    # face arrière
    glTexCoord2f(1, 1)
    glVertex3f(-.5, -.5, -.5)  # v0 (arrière)

    glTexCoord2f(1, 0)
    glVertex3f(-.5,  .5, -.5)  # v1 (arrière)

    glTexCoord2f(0, 1)
    glVertex3f( .5, -.5, -.5)  # v2 (arrière)

    glTexCoord2f(0, 0)
    glVertex3f( .5,  .5, -.5)  # v3 (arrière)

    # face droite
    glTexCoord2f(1, 1)
    glVertex3f( .5, -.5,  .5)  # v2 (avant)

    glTexCoord2f(1, 0)
    glVertex3f( .5,  .5,  .5)  # v3 (avant)

    # face avant
    glTexCoord2f(0, 1)
    glVertex3f(-.5, -.5,  .5)  # v0 (avant)

    glTexCoord2f(0, 0)
    glVertex3f(-.5,  .5,  .5)  # v1 (avant)

    # face gauche
    glTexCoord2f(1, 1)
    glVertex3f(-.5, -.5, -.5)  # v0 (arrière)

    glTexCoord2f(1, 0)
    glVertex3f(-.5,  .5, -.5)  # v1 (arrière)
    glEnd()


def draw_flooring():
    #
    #  v1 --- v2
    #   |     |
    #  v0 --- v3
    #

    glBegin(GL_QUADS)

    width = WORLD_DIM_X / 2 + .5
    height = WORLD_DIM_Y / 2 + .5

    glTexCoord2f(WORLD_DIM_X, 0)
    glVertex3f(-width, -.5, -height)  # v0

    glTexCoord2f(0, 0)
    glVertex3f(-width, -.5,  height)  # v1

    glTexCoord2f(0, WORLD_DIM_Y)
    glVertex3f( width, -.5,  height)  # v2

    glTexCoord2f(WORLD_DIM_X, WORLD_DIM_Y)
    glVertex3f( width, -.5, -height)  # v3

    glEnd()


def draw_ceiling():
    #
    #  v2 --- v1
    #   |     |
    #  v3 --- v0
    #

    glBegin(GL_QUADS)

    width = WORLD_DIM_X / 2 + .5
    height = WORLD_DIM_Y / 2 + .5

    glTexCoord2f(WORLD_DIM_X, WORLD_DIM_Y)
    glVertex3f( width, .5, -height)  # v3

    glTexCoord2f(0, WORLD_DIM_Y)
    glVertex3f( width, .5,  height)  # v2

    glTexCoord2f(0, 0)
    glVertex3f(-width, .5,  height)  # v1

    glTexCoord2f(WORLD_DIM_X, 0)
    glVertex3f(-width, .5, -height)  # v0

    glEnd()
