import time
import tkinter
from OpenGL import GL
from pyopengltk import OpenGLFrame

class AppOgl(OpenGLFrame):

    def initgl(self):
        """Initalize gl states when the frame is created"""
        GL.glViewport(0, 0, self.width, self.height)
        GL.glClearColor(0.0, 1.0, 0.0, 0.0)    
        self.start = time.time()
        self.nframes = 0

    def redraw(self):
        """Render a single frame"""
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        tm = time.time() - self.start
        self.nframes += 1
        print("fps",self.nframes / tm, end="\r" )


if __name__ == '__main__':
    """
    root = tkinter.Tk()
    canv = tkinter.Canvas(root, width=120, height=120)
    canv.pack()
    app = AppOgl(root, width=320, height=200)
    app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.animate = 1
    app.after(100, app.printContext)
    app.mainloop()
    """

    from graphic.drawerManager import DrawerManager
    from logic.utils.vec2D import Vec2D
    from logic.game.option import Option

    Option(window_dimensions=Vec2D(int(300 * 1.618), 600), fov=60)
    dm = DrawerManager()