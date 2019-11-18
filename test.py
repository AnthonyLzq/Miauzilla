import glfw
from math import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr


vertex_src = """
#version 310 es

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;

uniform mat4 rotation;

out vec3 v_color;

void main(){
    gl_Position = rotation * vec4(a_position, 1.0);
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

def window_resize(window, width, height):
    glViewport(0, 0, width, height)


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
glfw.set_window_size_callback(window, window_resize)

# Make the context current
glfw.make_context_current(window)

            #Vertices         #Colors
vertices = [-0.5, -0.5, 0.5,  1.0, 0.0, 0.0, 
            0.5, -0.5, 0.5,   0.0, 1.0, 0.0,
            0.5, 0.5, 0.5,   0.0, 0.0, 1.0,
            -0.5, 0.5, 0.5,   1.0, 1.0, 1.0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 
            0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
            0.5, 0.5, -0.5,   0.0, 0.0, 1.0,
            -0.5, 0.5, -0.5,  1.0, 1.0, 1.0]

indices =  [0, 1, 2, 2, 3, 0,
            4, 5, 6, 6, 7, 4,
            4, 5, 1, 1, 0, 4,
            6, 7, 3, 3, 2, 6,
            5, 6, 2, 2, 1, 5,
            7, 4, 0, 0, 3, 7]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

#position = glGetAttribLocation(shader, "a_position")
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

#color = glGetAttribLocation(shader, "a_color")
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(shader)
# glEnableClientState(GL_VERTEX_ARRAY)
# glVertexPointer(3, GL_FLOAT, 0, vertices)

# glEnableClientState(GL_COLOR_ARRAY)
# glColorPointer(3, GL_FLOAT, 0, colors)

glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
rotation_loc = glGetUniformLocation(shader, "rotation")

# The main aplication loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # ct = glfw.get_time()

    # glLoadIdentity()
    # glScale(abs(sin(ct)), abs(sin(ct)), 1)
    # glRotatef(sin(ct)*45, 0, 0, 1)
    # glTranslate(sin(ct), cos(ct), 0)
    # glDrawArrays(GL_TRIANGLES, 0, 3)
    # glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    rot_x = pyrr.Matrix44.from_x_rotation(0.5*glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.5*glfw.get_time())
    # glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x * rot_y)
    # glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x @ rot_y)
    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))


    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    glfw.swap_buffers(window)

# Terminate glfw, free alocated resources
glfw.terminate()
