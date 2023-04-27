from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pyopengltk import OpenGLFrame
import time
from math import cos, sin, atan, pi

import logic.game.game as game

MAP_WIDTH = 16
MAP_HEIGHT = 16

class OGLDrawer(OpenGLFrame):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.player = game.GAME.get_world().get_player()

    def initgl(self):
        """Initalize gl states when the frame is created"""
        self.start = time.time()
        self.nframes = 0

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glEnable(GL_LIGHTING)
        glShadeModel(GL_FLAT)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))

        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Fin du bloc init()

        glViewport(0, 0, self.width, self.height)
        glClearColor(0.0, 0.0, 0.0, 0.0)    
	
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        zNear = 0.1
        zFar = 5

        r = atan(pi / 6) * zNear
        t = 1/zFar/4

        glFrustum(-r, r, -t, t, zNear, zFar)

        glMatrixMode(GL_MODELVIEW)


    def redraw(self):
        """Render a single frame"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	
        glPushMatrix()
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, (1, 1, 1, 1))
        self.draw_flooring()
        self.draw_ceiling()
        
        # caméra
        glRotatef(self.player.get_rotation(), 1, 0, 0)
        #glRotatef(yaw, 0, 1, 0)
        glTranslatef(self.player.get_pos()[0], 0, self.player.get_pos()[1])
        
        glPushMatrix()
        glTranslatef(1, 0, -1)
        glColor4f(1, 1, .6, 1)
        self.draw_wall()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-1, 0, -1)
        glColor4f(1, 1, .6, 1)
        self.draw_wall()
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 0, -2)
        glColor4f(0, 1, .6, 1)
        self.draw_wall()
        glPopMatrix()
        
        glPopMatrix()
        #glutSwapBuffers()

        tm = time.time() - self.start
        self.nframes += 1
        print("fps",self.nframes / tm, end="\r" )

    def draw_wall(self):
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
        glVertex3f(-.5, -.5, -.5)  # v0 (arrière)
        glVertex3f(-.5,  .5, -.5)  # v1 (arrière)
        glVertex3f( .5, -.5, -.5)  # v2 (arrière)
        glVertex3f( .5,  .5, -.5)  # v3 (arrière)

        # face droite
        glVertex3f( .5, -.5,  .5)  # v2 (avant)
        glVertex3f( .5,  .5,  .5)  # v3 (avant)

        # face avant
        glVertex3f(-.5, -.5,  .5)  # v0 (avant)
        glVertex3f(-.5,  .5,  .5)  # v1 (avant)

        # face gauche
        glVertex3f(-.5, -.5, -.5)  # v0 (arrière)
        glVertex3f(-.5,  .5, -.5)  # v1 (arrière)
        glEnd()
            
    def draw_flooring(self):
        #
        #  v1 --- v2
        #   |     |
        #  v0 --- v3
        #

        glBegin(GL_QUADS)

        width = MAP_WIDTH / 2
        height = MAP_HEIGHT / 2

        glColor4f(.6, .6, .6, 1)
        glVertex3f(-width, -1, -height)  # v0
        glVertex3f(-width, -1,  height)  # v1
        glVertex3f( width, -1,  height)  # v2
        glVertex3f( width, -1, -height)  # v3

        glEnd()
            
    def draw_ceiling(self):
        #
        #  v2 --- v1
        #   |     |
        #  v3 --- v0
        #

        glBegin(GL_QUADS)

        width = MAP_WIDTH / 2
        height = MAP_HEIGHT / 2

        glColor4f(.4, .4, 1, 1)
        glVertex3f( width, 1, -height)  # v3
        glVertex3f( width, 1,  height)  # v2
        glVertex3f(-width, 1,  height)  # v1
        glVertex3f(-width, 1, -height)  # v0

        glEnd()