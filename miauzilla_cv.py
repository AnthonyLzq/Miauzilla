import glfw
from math import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
import random
from PIL import Image


vertex_src = """
#version 310 es

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;

uniform mat4 model; //combined translation and rotation
uniform mat4 projection;

out vec3 v_color;
out vec2 v_texture;

void main(){
    gl_Position = projection * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
#version 310 es

precision mediump float;

in vec2 v_texture; 

out vec4 out_color;

uniform sampler2D s_texture;

void main(){
    out_color = texture(s_texture, v_texture);
}
"""

            #Vertices          #Texture
vertices = [-0.5, -0.5,  0.5,  0.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,

            -0.5, -0.5, -0.5,  0.0, 0.0,
             0.5, -0.5, -0.5,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0,

             0.5, -0.5, -0.5,  0.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
             0.5, -0.5,  0.5,  0.0, 1.0,

            -0.5,  0.5, -0.5,  0.0, 0.0,
            -0.5, -0.5, -0.5,  1.0, 0.0,
            -0.5, -0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,

            -0.5, -0.5, -0.5,  0.0, 0.0,
             0.5, -0.5, -0.5,  1.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 1.0,

             0.5,  0.5, -0.5,  0.0, 0.0,
            -0.5,  0.5, -0.5,  1.0, 0.0,
            -0.5,  0.5,  0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  0.0, 1.0]
            

indices =  [0,  1,  2,  2,  3,  0,
            4,  5,  6,  6,  7,  4,
            8,  9, 10, 10, 11,  8,
            12, 13, 14, 14, 15, 12,
            16, 17, 18, 18, 19, 16,
            20, 21, 22, 22, 23, 20]


class Cube:
    def __init__(self):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        self.id_texture = 0
    
    def load_texture(self, file):
        self.id_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id_texture)

        # Set texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # load image
        images = [Image.open('./textures/ursa.png'), Image.open('./textures/cat.png')]
        for i in range(len(images)):
            images[i] = images[i].transpose(Image.FLIP_TOP_BOTTOM)

        image_data = images[0].convert("RGBA").tobytes(), images[1].convert("RGBA").tobytes()

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, images[file].width, images[file].height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data[file])

class Window:
    def __init__(self, width: int, height: int, title: str):
        if not glfw.init():
            raise Exception("glfw can not be initilized")

        self.win = glfw.create_window(width, height, title, None, None)

        if not self.win:
            glfw.terminate()
            raise Exception("glfw can not be created!")

        glfw.set_window_pos(self.win, 400, 200)
        glfw.set_window_size_callback(self.win, self.window_resize)
        glfw.make_context_current(self.win)

    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, 100)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


class Shader:
    def __init__(self, cubes):        
        self.shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

        # Vertex Buffer Object
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        for cube in cubes:
            glBufferData(GL_ARRAY_BUFFER, cube.vertices.nbytes, cube.vertices, GL_STATIC_DRAW)

        # Element Buffer Object
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        for cube in cubes:
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube.indices.nbytes, cube.indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        for cube in cubes:
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.vertices.itemsize * 5, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        for cube in cubes:
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.vertices.itemsize * 5, ctypes.c_void_p(12))

# Creating the window
main_window = Window(1080, 720, "Miauzilla")

my_cubes = [0]*30
for i in range(30):
    my_cubes[i] = Cube()
    my_cubes[i].load_texture(1)

main_shader = Shader(my_cubes)

glUseProgram(main_shader.shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1080/720, 0.1, 100)

initial_cube_position = [0]*30
for i in range(30):
    initial_cube_position[i] = pyrr.Vector3([
                        random.randrange(-5.0, 5.0), 
                        0.0, 
                        random.randrange(-100, -40)])
# initial_cube_position[0] = pyrr.Vector3([1.0, 0.0, -10.0])
# initial_cube_position[1] = pyrr.Vector3([-1.0, 0.0, -10.0])
# initial_cube_position[2] = pyrr.Vector3([0.0, 1.0, -15.0])

matrix_cube_translation = [0]*30
for i in range(30):
    matrix_cube_translation[i] = pyrr.matrix44.create_from_translation(initial_cube_position[i])
# matrix_cube_translation[0] = pyrr.matrix44.create_from_translation(initial_cube_position[0])
# matrix_cube_translation[1] = pyrr.matrix44.create_from_translation(initial_cube_position[1])
# matrix_cube_translation[2] = pyrr.matrix44.create_from_translation(initial_cube_position[2])

# eye, target, up
# view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 3]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(main_shader.shader, "model")
proj_loc = glGetUniformLocation(main_shader.shader, "projection")
view_loc = glGetUniformLocation(main_shader.shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
# glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

def main():
    translate_cube_z = pyrr.Vector3([0.0, 0.0, 0.1])
    # The main aplication loop
    while not glfw.window_should_close(main_window.win):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_x = pyrr.Matrix44.from_x_rotation(0.5*glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.5*glfw.get_time())
        rotation = 1#pyrr.matrix44.multiply(rot_x, rot_y)

        # initial_cube_position[0] += translate_cube_z

        for i in range(30):
            initial_cube_position[i] += translate_cube_z
            model = pyrr.matrix44.multiply(rotation, matrix_cube_translation[i])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
            matrix_cube_translation[i] = pyrr.matrix44.create_from_translation(initial_cube_position[i])

        glfw.swap_buffers(main_window.win)

    # Terminate glfw, free alocated resources
    glfw.terminate()

if __name__ == '__main__':
    main()