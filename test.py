import glfw
from OpenGL.GL import *
from math import *
import numpy as np

# Initializing glfw library
if not glfw.init():
    raise Exception("Glfw can not be initialazed!")

# Creating the window
window = glfw.create_window(1080, 640, "My OpenGl Window", None, None)

# Check if the window was created
if not window:
    glfw.terminate()
    # Return the elapsed time, since init was called
    raise Exception('Glfw can not be created!')

# Set window's position
glfw.set_window_pos(window, 400, 200)

# Make the context current
glfw.make_context_current(window)

vertices = [-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0, 0.5, 0.0]

colors = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

vertices = np.array(vertices, dtype=np.float32)
colors = np.array(colors, dtype=np.float32)

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(3, GL_FLOAT, 0, vertices)

glEnableClientState(GL_COLOR_ARRAY)
glColorPointer(3, GL_FLOAT, 0, colors)

glClearColor(0, 0.1, 0.1, 1)

# The main aplication loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    ct = glfw.get_time()

    glLoadIdentity()
    glScale(abs(sin(ct)), abs(sin(ct)), 1)
    glRotatef(sin(ct)*45, 0, 0, 1)
    glTranslate(sin(ct), cos(ct), 0)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glfw.swap_buffers(window)

# Terminate glfw, free alocated resources
glfw.terminate()
