from __future__ import annotations

from math import pi, tan, sqrt

import numpy
from OpenGL.GL import *
from pyopengltk import OpenGLFrame

import logic.game.game as game
from logic.world.blockType import BlockType
from logic.world.world import WORLD_DIM_X, WORLD_DIM_Y

GOD_MODE = False
"""
Affiche une vue du dessus de la map.
"""


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

        if not GOD_MODE:
            glEnable(GL_CULL_FACE)

        # glEnable(GL_LIGHTING)
        glShadeModel(GL_FLAT)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))

        # Textures

        _bytes = numpy.load("../res/img/img.png.baked", allow_pickle=True)

        glBindTexture(GL_TEXTURE_2D, 1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB8, 2048, 2048, 0, GL_RGB, GL_UNSIGNED_BYTE, _bytes)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glGenerateMipmap(GL_TEXTURE_2D)

        print("GL_ERROR:", glGetError())

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

        glMatrixMode(GL_MODELVIEW)

    def redraw(self):
        """
        Render a single frame.
        """

        # Remarque:
        #   Mon +x est son -x, d'où les magouilles dans la composante x.

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	

        glPushMatrix()
        glMaterialfv(GL_FRONT, GL_AMBIENT, (1, 1, 1, 1))

        # Caméra
        if not GOD_MODE:
            OGLDrawer.draw_flooring()
            OGLDrawer.draw_ceiling()

            glRotatef(180, 1, 0, 0)
            glRotatef(-self.player.get_rotation() + 90, 0, 1, 0)
            glTranslatef(-(WORLD_DIM_X - self.player.get_pos()[0]), 0, -self.player.get_pos()[1])
        else:
            glRotatef(-90, 1, 0, 0)
            glRotatef(self.player.get_rotation() + 90, 0, 1, 0)
            glTranslatef(-(WORLD_DIM_X - self.player.get_pos()[0]), 10, -self.player.get_pos()[1])

        glEnable(GL_TEXTURE_2D)
        glColor4f(1, 1, 1, 1)

        # Murs
        for x in range(WORLD_DIM_X):
            for y in range(WORLD_DIM_Y):
                if self.player.world.world_matrix[y][x] == BlockType.WALL:
                    glPushMatrix()
                    glTranslatef(WORLD_DIM_X - x, 0, y)
                    OGLDrawer.draw_wall()
                    glPopMatrix()

        glDisable(GL_TEXTURE_2D)
        
        glPopMatrix()

    @staticmethod
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
        glTexCoord2f(1, 0)
        glVertex3f(-.5, -.5, -.5)  # v0 (arrière)

        glTexCoord2f(1, 1)
        glVertex3f(-.5,  .5, -.5)  # v1 (arrière)

        glTexCoord2f(0, 0)
        glVertex3f( .5, -.5, -.5)  # v2 (arrière)

        glTexCoord2f(0, 1)
        glVertex3f( .5,  .5, -.5)  # v3 (arrière)

        # face droite
        glTexCoord2f(1, 0)
        glVertex3f( .5, -.5,  .5)  # v2 (avant)

        glTexCoord2f(1, 1)
        glVertex3f( .5,  .5,  .5)  # v3 (avant)

        # face avant
        glTexCoord2f(0, 0)
        glVertex3f(-.5, -.5,  .5)  # v0 (avant)

        glTexCoord2f(0, 1)
        glVertex3f(-.5,  .5,  .5)  # v1 (avant)

        # face gauche
        glTexCoord2f(1, 0)
        glVertex3f(-.5, -.5, -.5)  # v0 (arrière)

        glTexCoord2f(1, 1)
        glVertex3f(-.5,  .5, -.5)  # v1 (arrière)
        glEnd()

    @staticmethod
    def draw_flooring():
        #
        #  v1 --- v2
        #   |     |
        #  v0 --- v3
        #

        glBegin(GL_QUADS)

        width = WORLD_DIM_X * 2
        height = WORLD_DIM_Y * 2

        glColor4f(.6, .6, .6, 1)
        glVertex3f(-width, -1, -height)  # v0
        glVertex3f(-width, -1,  height)  # v1
        glVertex3f( width, -1,  height)  # v2
        glVertex3f( width, -1, -height)  # v3

        glEnd()

    @staticmethod
    def draw_ceiling():
        #
        #  v2 --- v1
        #   |     |
        #  v3 --- v0
        #

        glBegin(GL_QUADS)

        width = WORLD_DIM_X * 2
        height = WORLD_DIM_Y * 2

        glColor4f(.4, .4, 1, 1)
        glVertex3f( width, 1, -height)  # v3
        glVertex3f( width, 1,  height)  # v2
        glVertex3f(-width, 1,  height)  # v1
        glVertex3f(-width, 1, -height)  # v0

        glEnd()
