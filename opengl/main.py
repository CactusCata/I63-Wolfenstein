from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import atan, pi, cos, sin

MAP_WIDTH = 1024
MAP_HEIGHT = 1024

yaw = 0
pitch = 0
x = 0
z = 0

def init():
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_CULL_FACE)
	
	glEnable(GL_LIGHTING)
	glShadeModel(GL_FLAT)
	
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))
	
	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
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
	
	def draw_flooring():
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
	
	def draw_ceiling():
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
	
	glPushMatrix()
	
	glMaterialfv(GL_FRONT, GL_AMBIENT, (1, 1, 1, 1))
	draw_flooring()
	draw_ceiling()
	
	# caméra
	glRotatef(pitch, 1, 0, 0)
	glRotatef(yaw, 0, 1, 0)
	glTranslatef(x, 0, z)
	
	glPushMatrix()
	glTranslatef(1, 0, -1)
	glColor4f(1, 1, .6, 1)
	draw_wall()
	glPopMatrix()
	
	glPushMatrix()
	glTranslatef(-1, 0, -1)
	glColor4f(1, 1, .6, 1)
	draw_wall()
	glPopMatrix()
	
	glPushMatrix()
	glTranslatef(0, 0, -2)
	glColor4f(0, 1, .6, 1)
	draw_wall()
	glPopMatrix()
	
	glPopMatrix()
	glutSwapBuffers()


def reshape(width, height):
	glViewport(0, 0, width, height)
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	
	zNear = 0.1
	zFar = 5
	
	r = atan(pi / 6) * zNear
	t = 1/zFar/4
	
	glFrustum(-r, r, -t, t, zNear, zFar)
	
	glMatrixMode(GL_MODELVIEW)


def keyboard(key, _x, _y):
	global yaw, pitch, x, z
	
	key = key.decode('utf-8')
	
	if key == '\033':
		glutLeaveMainLoop()
	
	elif key == 'd':
		yaw = (yaw + 5) % 360
		
	elif key == 'q':
		yaw = (yaw - 5) % 360
	
	elif key == 'z':
		x -= sin(yaw * pi/180) * 1/8
		z += cos(yaw * pi/180) * 1/8
	
	elif key == 's':
		x += sin(yaw * pi/180) * 1/8
		z -= cos(yaw * pi/180) * 1/8
	
	glutPostRedisplay()


if __name__ == "__main__":
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
	glutCreateWindow("Projet")
	glutReshapeWindow(320, 200)

	glutReshapeFunc(reshape)
	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard)

	init()
	glutMainLoop()

