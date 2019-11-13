import glfw
from math import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np


vertex_src = """
#version 310 es

in vec3 a_position;
in vec3 a_color;

out vec3 v_color;

void main(){
    gl_Position = vec4(a_position, 1.0);
    v_color = a_color;
}
"""

fragment_src = """
#version 310 es

precision mediump float;

in vec3 v_color;
out vec4 out_color;

void main(){
    out_color = vec4(v_color, 1.0);
}
"""

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

            #Vertices        #Colors
vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0]

vertices = np.array(vertices, dtype=np.float32)

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

position = glGetAttribLocation(shader, "a_position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

color = glGetAttribLocation(shader, "a_color")
glEnableVertexAttribArray(color)
glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(shader)
# glEnableClientState(GL_VERTEX_ARRAY)
# glVertexPointer(3, GL_FLOAT, 0, vertices)

# glEnableClientState(GL_COLOR_ARRAY)
# glColorPointer(3, GL_FLOAT, 0, colors)

glClearColor(0, 0.1, 0.1, 1)

# The main aplication loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)

    # ct = glfw.get_time()

    # glLoadIdentity()
    # glScale(abs(sin(ct)), abs(sin(ct)), 1)
    # glRotatef(sin(ct)*45, 0, 0, 1)
    # glTranslate(sin(ct), cos(ct), 0)
    # glDrawArrays(GL_TRIANGLES, 0, 3)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glfw.swap_buffers(window)

# Terminate glfw, free alocated resources
glfw.terminate()
