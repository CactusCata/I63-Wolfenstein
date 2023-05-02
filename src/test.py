from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image

from math import sqrt

y = 0.0
x = 0.0
z = -5.0

rot_x_cam = 0.0
rot_y_cam = 0.0
rot_z_cam = 0.0

rot_mode = 0

day = 0
year = 0

bayer = True

texture_id = 0

def create_vect(A, B):
    return (B[0] - A[0], B[1] - A[1], B[2] - A[2])

def produit_vectoriel(v1, v2):
    return (v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0])

def produit_scalaire(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]

def norme(vec):
    return sqrt(produit_scalaire(vec, vec))

def get_normal(A, B, C):
    u = create_vect(A, B)
    v = create_vect(B, C)
    N = produit_vectoriel(u, v)
    norme_N = norme(N)
    N = (N[0] / norme_N, N[1] / norme_N, N[2] / norme_N)
    return N

def generate_triangles_normal(triangles):
    normales = []
    for triangle in triangles:
        normales.append(get_normal(triangle[0], triangle[1], triangle[2]))
    return normales

def init():
    # Permet de normaliser les normales des sommets
    #glEnable(GL_NORMALIZE)

    glFrontFace(GL_CW)

    # Permet de rendre les faces avant, arrière ou les deux
    glEnable(GL_CULL_FACE)

    glEnable(GL_TEXTURE_2D)

    # Permet l'application d'une matrice de Bayer pour
    # donner l'illusion de smooth pour une bande de couleur
    # qui possède peu de différentes couleurs
    #glEnable(GL_DITHER)

    # Couleur de utilisée pour nettoyer l'écran
    glClearColor(0.0, 0.0, 0.0, 0.0)

    # FLAT (une couleur), GOURAUD (autre), SMOOTH (PHUNG)
    # modèle d'ombrage à utiliser lors du rendu des objets 3D.
    glShadeModel(GL_SMOOTH)

    # L'application traite vraiment
    # le buffer de profondeur
    glEnable(GL_DEPTH_TEST)

def draw_bar(p, q):
    w = q[0] - p[0]
    h = q[1] - p[1]
    d = q[2] - p[2]

    glColor(0.1, 0.1, 0.1)

    # Face avant
    normal = get_normal((p[0], p[1], p[2]), (p[0] + w, p[1], p[2]), (p[0] + w, p[1] + h, p[2]))
    glNormal3f(normal[0], normal[1], normal[2])
    glBegin(GL_QUADS)
    glVertex3f(p[0], p[1], p[2])
    glVertex3f(p[0] + w, p[1], p[2])
    glVertex3f(p[0] + w, p[1] + h, p[2])
    glVertex3f(p[0], p[1] + h, p[2])
    glEnd()

    normal = get_normal((p[0], p[1], p[2] + d), (p[0], p[1] + h, p[2] + d), (p[0] + w, p[1] + h, p[2] + d))
    glNormal3f(normal[0], normal[1], normal[2])
    glBegin(GL_QUADS)
    glVertex3f(p[0], p[1], p[2] + d)
    glVertex3f(p[0], p[1] + h, p[2] + d)
    glVertex3f(p[0] + w, p[1] + h, p[2] + d)
    glVertex3f(p[0] + w, p[1], p[2] + d)
    glEnd()

    normal = get_normal((p[0], p[1] + h, p[2]), (p[0], p[1] + h, p[2] + d), (p[0] + w, p[1] + h, p[2] + d))
    glNormal3f(normal[0], normal[1], normal[2])
    glBegin(GL_QUADS)
    glVertex3f(p[0], p[1] + h, p[2])
    glVertex3f(p[0] + w, p[1] + h, p[2])
    glVertex3f(p[0] + w, p[1] + h, p[2] + d)
    glVertex3f(p[0], p[1] + h, p[2] + d)
    glEnd()

    normal = get_normal((p[0], p[1], p[2]), (p[0], p[1], p[2] + d), (p[0] + w, p[1], p[2] + d))
    glNormal3f(normal[0], normal[1], normal[2])
    glBegin(GL_QUADS)
    glVertex3f(p[0], p[1], p[2])
    glVertex3f(p[0], p[1], p[2] + d)
    glVertex3f(p[0] + w, p[1], p[2] + d)
    glVertex3f(p[0] + w, p[1], p[2])
    glEnd()

    normal = get_normal((p[0], p[1], p[2]), (p[0], p[1] + h, p[2]), (p[0], p[1] + h, p[2] + d))
    glNormal3f(normal[0], normal[1], normal[2])
    glBegin(GL_QUADS)
    glVertex3f(p[0], p[1], p[2])
    glVertex3f(p[0], p[1] + h, p[2])
    glVertex3f(p[0], p[1] + h, p[2] + d)
    glVertex3f(p[0], p[1], p[2] + d)
    glEnd()
    
    normal = get_normal((p[0] + w, p[1], p[2]), (p[0] + w, p[1], p[2] + d), (p[0] + w, p[1] + h, p[2] + d))
    glNormal3f(normal[0], normal[1], normal[2])
    glBegin(GL_QUADS)
    glVertex3f(p[0] + w, p[1], p[2])
    glVertex3f(p[0] + w, p[1], p[2] + d)
    glVertex3f(p[0] + w, p[1] + h, p[2] + d)
    glVertex3f(p[0] + w, p[1] + h, p[2])
    glEnd()

def draw_plan(from_, to_, step, delta=0.05):
    t = from_
    while t <= to_:
        draw_bar((from_, 0 - delta, t - delta), (to_, 0 + delta, t + delta))
        draw_bar((t - delta, 0 - delta, from_), (t + delta, 0 + delta, to_))
        t += step

def draw_triangle(points, colors):
    normal = get_normal(points[0], points[1], points[2])

    glBegin(GL_TRIANGLES)

    for i in range(3):
        glColor3f(colors[i][0], colors[i][1], colors[i][2])
        glNormal3f(normal[0], normal[1], normal[2])
        glVertex3f(points[i][0], points[i][1], points[i][2])

    glEnd()


def draw_pyramid(points):

    #glPushMatrix()

    # Exclu les faces arrières
    #glCullFace(GL_BACK)

    colors = [(1.0, 0.0, 0.0),
              (1.0, 1.0, 0.0),
              (0.0, 1.0, 0.0),
              (0.0, 1.0, 1.0),
              (0.0, 0.0, 1.0)]

    draw_triangle([points[0], points[3], points[4]], [colors[0], colors[3], colors[4]])
    draw_triangle([points[0], points[1], points[3]], [colors[0], colors[1], colors[3]])
    draw_triangle([points[0], points[2], points[1]], [colors[0], colors[2], colors[1]])
    draw_triangle([points[0], points[4], points[2]], [colors[0], colors[4], colors[2]])

    glBegin(GL_TRIANGLE_STRIP)

    glColor3f(0.3, 0.3, 0.3)
    normal = get_normal(points[1], points[2], points[3])

    for i in range(1, 5):
        glNormal3f(normal[0], normal[1], normal[2])
        glVertex3f(points[i][0], points[i][1], points[i][2])

    glEnd()

    #glPopMatrix()

def draw_cube(x, z):
    glBegin(GL_QUADS)
    # Front face
    coef = 0.5

    # Top face
    glTexCoord2f(0.0, 1.0); glNormal3f(0, 1, 0); glVertex3f(-coef + x,  0, -coef + z)
    glTexCoord2f(0.0, 0.0); glNormal3f(0, 1, 0); glVertex3f(-coef + x,  0,  coef + z)
    glTexCoord2f(1.0, 0.0); glNormal3f(0, 1, 0); glVertex3f( coef + x,  0,  coef + z)
    glTexCoord2f(1.0, 1.0); glNormal3f(0, 1, 0); glVertex3f( coef + x,  0, -coef + z)

    glEnd()

def display():
    # Clear l'ecran
    # Clear le Z-buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    glPushMatrix()
    glTranslatef(x, y, z)
    #draw_plan(-10, 10, 1, 0.02)
    glRotatef(rot_x_cam, 1.0, 0.0, 0.0)
    glRotatef(rot_y_cam, 0.0, 1.0, 0.0)
    glRotatef(rot_z_cam, 0.0, 0.0, 1.0)
    glScalef(0.5, 0.5, 0.5)
    

    for a in range(-100, 100):
        for b in range(-100, 10):
            draw_cube(a, b)
    #glBindTexture(GL_TEXTURE_2D, 0) # Détacher la texture

    # pour le placement de la lune,
    # il ne  faut pas prendre en compte la
    # rotation de la terre, donc pop après la rotation
    # de la terre puis je dessine la lune

    # De base on travaille sur une matrice courante
    # Avec une pile de matrice, on peut changer
    # l'état de la matrice courante avec un état antérieur

    """
    draw_pyramid([
        (+0.0, +2.0, +0.0),
        (-1.0, +0.0, +1.0),
        (+1.0, +0.0, +1.0),
        (-1.0, +0.0, -1.0),
        (+1.0, +0.0, -1.0)
    ])

    draw_pyramid([
        (+6.0, +3.0, +2.0),
        (+5.5, +2.0, +2.5),
        (+6.5, +2.0, +2.5),
        (+5.5, +2.0, +1.5),
        (+6.5, +2.0, +1.5)
    ])
    """
    glPopMatrix()
    


    glutSwapBuffers()




def load_texture(filename):
    img = Image.open(filename).convert('RGB')
    img_data = img.tobytes("raw", "RGBX", 0, -1)
    width, height = img.size
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    print(texture_id)
    return texture_id

def keyboard(key, _x, _y):
    global x, y, z, bayer, rot_x_cam, rot_y_cam, rot_z_cam
    key = key.decode('utf-8')
    if key == 'z':
        z += 0.1
    elif key == 's':
        z -= 0.1
    elif key == 'q':
        x += 0.1
    elif key == 'd':
        x -= 0.1
    elif key == ' ':
        y -= 0.1
    elif key == 'k':
        rot_x_cam += 10
    elif key == 'l':
        rot_y_cam += 10
    elif key == 'm':
        rot_z_cam += 10
    elif key == 'c':
        y += 0.1
    elif key == 'b':
        if (bayer):
            bayer = False
            glDisable(GL_DITHER)
        else:
            bayer = True
            glEnable(GL_DITHER)
    elif key == '\033':
        # sys.exit( )  # Exception ignored
        glutLeaveMainLoop()
    glutPostRedisplay()  # indispensable en Python

def reshape(width, height):
    global ar
    # On dit que la fenetre de dessin fait toute la fenetre
    glViewport(0, 0, width, height)

    ar = 0
    if width <= height:
        ar = height / width
    else:
        ar = width / height

    # indique à OpenGL que les opérations de transformation 
    # suivantes doivent être appliquées à la matrice de projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # angle, ratio, near, far
    gluPerspective(100, ar, 0.1, 20)
    glMatrixMode(GL_MODELVIEW)
    #glLoadIdentity()
    #gluLookAt(0.0, 0.0, -5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


if __name__ == "__main__":

    glutInit(len(sys.argv), sys.argv)
    # Option GLUT_DOUBLE: travail avec deux buffer d'affichage: c'est un swap buffer
    # Option GLUT_RGBA  : travail avec le quadruplet rouge,vert,bleu,alpha
    # Option GLUT_DEPTH : travail avec un buffer de profondeur (le Z-buffer)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutCreateWindow('test')
    glutReshapeWindow(512,512)

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)

    init()
    texture_id = load_texture("../res/img/roof_tile_2.png")
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glutMainLoop()