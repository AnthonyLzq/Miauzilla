import glfw
import pyrr
import random
import pygame
import os
import numpy as np

from math import *
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


# This variable handles the position, texture and view of any OpenGL object that is created with the shader program
vertex_src = """
#version 310 es

precision mediump float;

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model; //translation
uniform mat4 projection;
uniform mat4 view;

out vec3 v_normal;
out vec2 v_texture;

void main(){
    v_normal = normalize((model * vec4(floor(a_normal), 0)).xyz);
    v_texture = a_texture;
    gl_Position = projection * view * model * vec4(a_position, 1.0);
}
"""

# This variable "encapsulates" the texture (image) that we want to use with the type of texture (2D in this case), and ir returns a texture 2D with the image we wanted.
fragment_src = """
#version 310 es

precision mediump float;

in vec2 v_texture; 
in vec3 v_normal;

out vec4 out_texture;

uniform vec3 light_direction;
uniform sampler2D s_texture;

void main(){
    float diffuse = max(dot(v_normal, light_direction), 0.0);
    float ambient = 0.3;
    float lighting = max(diffuse, ambient);
    
    vec4 sample1 = texture2D(s_texture, v_texture);
    out_texture = vec4(sample1.xyz * lighting, sample1.a);
}
"""

quad_vertices = [#Vertices               #Texture       #Light
                -10.0, -0.5,  20.0,      0.0, 0.0,      0.0,  1.0,  0.0,  
                 10.0, -0.5,  20.0,      1.0, 0.0,      0.0,  1.0,  0.0,
                 10.0, -0.5,  -10000,    1.0, 1.0,      0.0,  1.0,  0.0,
                -10.0, -0.5,  -10000,    0.0, 1.0,      0.0,  1.0,  0.0]


quad_indices = [0, 1, 2, 2, 3, 0]


cube_vertices = [#Vertices          #Texture     #Light
                -0.5, -0.5,  0.5,   0.0, 0.0,    0.0,  0.0,  1.0,  
                 0.5, -0.5,  0.5,   1.0, 0.0,    0.0,  0.0,  1.0,  
                 0.5,  0.5,  0.5,   1.0, 1.0,    0.0,  0.0,  1.0,  
                -0.5,  0.5,  0.5,   0.0, 1.0,    0.0,  0.0,  1.0,  

                -0.5, -0.5, -0.5,   0.0, 0.0,    0.0,  0.0, -1.0,
                 0.5, -0.5, -0.5,   1.0, 0.0,    0.0,  0.0, -1.0,
                 0.5,  0.5, -0.5,   1.0, 1.0,    0.0,  0.0, -1.0,
                -0.5,  0.5, -0.5,   0.0, 1.0,    0.0,  0.0, -1.0,

                 0.5, -0.5, -0.5,   0.0, 0.0,    1.0,  0.0, -1.0,
                 0.5,  0.5, -0.5,   1.0, 0.0,    1.0,  0.0, -1.0,
                 0.5,  0.5,  0.5,   1.0, 1.0,    1.0,  0.0, -1.0,
                 0.5, -0.5,  0.5,   0.0, 1.0,    1.0,  0.0, -1.0,

                -0.5,  0.5, -0.5,   0.0, 0.0,   -1.0,  0.0,  0.0,
                -0.5, -0.5, -0.5,   1.0, 0.0,   -1.0,  0.0,  0.0,
                -0.5, -0.5,  0.5,   1.0, 1.0,   -1.0,  0.0,  0.0,
                -0.5,  0.5,  0.5,   0.0, 1.0,   -1.0,  0.0,  0.0,

                -0.5, -0.5, -0.5,   0.0, 0.0,    0.0, -1.0, -1.0,
                 0.5, -0.5, -0.5,   1.0, 0.0,    0.0, -1.0, -1.0,
                 0.5, -0.5,  0.5,   1.0, 1.0,    0.0, -1.0, -1.0,
                -0.5, -0.5,  0.5,   0.0, 1.0,    0.0, -1.0, -1.0,

                 0.5,  0.5, -0.5,   0.0, 0.0,    0.0,  1.0, -1.0,
                -0.5,  0.5, -0.5,   1.0, 0.0,    0.0,  1.0, -1.0,
                -0.5,  0.5,  0.5,   1.0, 1.0,    0.0,  1.0, -1.0,
                 0.5,  0.5,  0.5,   0.0, 1.0,    0.0,  1.0, -1.0]
            

cube_indices =  [0,  1,  2,  2,  3,  0,
                4,  5,  6,  6,  7,  4,
                8,  9, 10, 10, 11,  8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]

# List that stores textures
texture_surface = [  
                Image.open('./textures/02-obstacle.png'), 
                Image.open('./textures/02-obstacle-2.png'),
                Image.open('./textures/01-character.png'),
                Image.open('./textures/03-ground.png'),
                Image.open('./textures/04-sky.png')]

# Setting the quantity of obstacles
n = 35

# Setting the position of the cubes that conform the cat
gato = [[0.0, 0.5, -4.5], # body 1/2
        [0.0, 0.5, -3.5], # body 2/2 
        [0.0, 0.5, -2.5], # tail 1/3
        [0.0, 0.5, -1.5], # tail 2/3
        [0.0, 0.5, -0.5], # tail 2/3
        [0.0, 1.0, -5.0], # head 1/2
        [0.0, 1.0, -5.5], # head 2/2    
        [0.25, 0.0, -3.25], # right back leg
        [-0.25, 0.0, -3.25], # left back leg
        [0.25, 0.0, -4.75], # right frong leg
        [-0.25, 0.0, -4.75]] # left front leg


gato_escala = [
                [1.0, 1.0, 1.0], # body 1/2
                [1.0, 1.0, 1.0], # body 2/2
                [0.5, 0.5, 1.0], # tail 1/3
                [0.3, 0.3, 1.0], # tail 2/3
                [0.2, 0.2, 1.0], # tail 2/3
                [1.0, 1.0, 1.0], # head 1/2
                [0.5, 0.5, 0.5], # head 2/2
                [0.25, 1.0, 0.25], # right back leg
                [0.25, 1.0, 0.25], # left back legizquierda
                [0.25, 1.0, 0.25], # right front leg
                [0.25, 1.0, 0.25]] # left front leg

# Setting the quantity of cubes that conform the cat
m = len(gato)

# Reversing the images to be properly render
for i in range(len(texture_surface)):
    texture_surface[i] = texture_surface[i].transpose(Image.FLIP_TOP_BOTTOM)

texture_data = [0]*len(texture_surface)
for i in range(len(texture_data)):
    texture_data[i] = texture_surface[i].convert("RGBA").tobytes()

class Cube:
    '''
    This class represents the cubes that will be render in the main window.
    Vertices are initialized by modifying the "cube vertices" and "cube indices" constants that are lines below. They became numpy arrays instead of lists.    Esta clase contiene los siguientes 
    
    This class has the following methods:
        - load_texture: it's responsible for wrapping the cube with a texture passed as a parameter.
    '''
    def __init__(self):
        # Conversion from array to numpy array, for vertices and indices.
        self.cube_vertices = np.array(cube_vertices, dtype=np.float32)
        self.cube_indices = np.array(cube_indices, dtype=np.uint32)
        self.id_texture = 0
    
    def load_texture(self, file):
        # Generating a texture and saving it in the id
        self.id_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id_texture)
        # Set texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface[file].width, texture_surface[file].height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data[file])

class Ground:
    '''
    Esta clase representará será la que permitirá renderizar el suelo y también en el cielo, para esto se utilizará un cuadrado.
    This class will represent the ground and sky, for this a quad will be used.

    This class has de following methods:
    - load_texture: it's resposible for wrapping the quad with a texture passed as a parameter.

    '''
    def __init__(self):
        self.quad_vertices = np.array(quad_vertices, dtype=np.float32)
        self.quad_indices = np.array(quad_indices, dtype=np.uint32)
        self.id_texture = 0

    def load_texture(self, file):
        self.id_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_surface[file].width, texture_surface[file].height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data[file])


class Window:
    '''
    This class is the one that represents the main window where the game takes place, it is initialized receiving as parameters a width, length and a title.
    The window is created by default in the position (400, 200).
    
    This class has the following methods:
        - window_resize: it is the callback that is executed when there is a window resize.
    '''
    # Constructor
    def __init__(self, width: int, height: int, title: str):
        if not glfw.init():
            raise Exception("glfw can not be initilized")

        # Initializing the window
        self.win = glfw.create_window(width, height, title, None, None)
        self.mode_perspective = 0
        self.light_perspective = 0

        if not self.win:
            glfw.terminate()
            raise Exception("glfw can not be created!")

        glfw.set_window_pos(self.win, 400, 200)
        glfw.make_context_current(self.win)
        glfw.set_window_size_callback(self.win, self.window_resize)

    # Callback method that handles the window resize
    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, 1000)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    # Method that handles with the key events
    def key_event(self, window, key, scancode, action, mods):
        global view, n, m, cube_position

        # Key to exit the game
        if action == glfw.PRESS and key == glfw.KEY_Q:
            if self.mode_perspective == 0:
                view = pyrr.matrix44.create_look_at(pyrr.Vector3([10, 8, 3]), pyrr.Vector3([0, 1.5, 0]), pyrr.Vector3([0, 1, 0]))
                self.mode_perspective += 1
            elif self.mode_perspective == 1:
                view = pyrr.matrix44.create_look_at(pyrr.Vector3([-10, 8, 3]), pyrr.Vector3([0, 1.5, 0]), pyrr.Vector3([0, 1, 0]))
                self.mode_perspective += 1
            else:
                view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 2, 3]), pyrr.Vector3([0, 1.5, -1]), pyrr.Vector3([0, 1, 0]))
                self.mode_perspective = 0

        # Handling with the position of the light
        if action == glfw.PRESS and key == glfw.KEY_E:
            global light_loc
            if self.mode_perspective == 0:
                glUniform3f(light_loc, 0.0, 0.0, 1.0)
                self.mode_perspective += 1
            elif self.mode_perspective == 1:
                glUniform3f(light_loc, 0.0, 1.0, 0.0)
                self.mode_perspective += 1
            elif self.mode_perspective == 2:
                glUniform3f(light_loc, 1.0, 0.0, 0.0)
                self.mode_perspective = 0

        # Dealing with movement of the cat
        if action == glfw.PRESS and (key == glfw.KEY_A or key == glfw.KEY_LEFT):
            translate_cube_x = pyrr.Vector3([-0.5, 0.0, 0.0])
            for i in range(m):
                cube_position[n+i] += translate_cube_x
        elif action == glfw.PRESS and (key == glfw.KEY_D or key == glfw.KEY_RIGHT):
            translate_cube_x = pyrr.Vector3([+0.5, 0.0, 0.0])
            for i in range(m):
                cube_position[n+i] += translate_cube_x
        elif action == glfw.PRESS and (key == glfw.KEY_S or key == glfw.KEY_DOWN):
            translate_cube_z = pyrr.Vector3([0.0, 0.0, +0.5])
            for i in range(m):
                cube_position[n+i] += translate_cube_z
        elif action == glfw.PRESS and (key == glfw.KEY_W or key == glfw.KEY_UP):
            translate_cube_z = pyrr.Vector3([0.0, 0.0, -0.5])
            for i in range(m):
                cube_position[n+i] += translate_cube_z


class Shader:
    '''
    This class will represent the shader that will use the program to render OpenGl objects.

    This class has the following methods
        - vinculate_cubes: associate each cube in a list of cubes using a VAO, VBO and EBO.
        - vinculate_ground: associate the ground using VAO, VBO and EBO.
        - vinculate_sky: associate the sky using VAO, VBO and EBO.
    '''
    def __init__(self):        
        self.shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    def vinculate_cubes(self, cubes):
        global n,m
        self.cube_VAO = [0]*(n+m)
        self.cube_VBO = [0]*(n+m)
        self.cube_EBO = [0]*(n+m)

        for x, cube in enumerate(cubes):
            # Vertex array object for each cube in cubes
            self.cube_VAO[x] = glGenVertexArrays(1)
            glBindVertexArray(self.cube_VAO[x])

            # Vertex Buffer Object for each cube in cubes
            self.cube_VBO[x] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.cube_VBO[x])
            glBufferData(GL_ARRAY_BUFFER, cube.cube_vertices.nbytes, cube.cube_vertices, GL_STATIC_DRAW)

            # Element Buffer Object for each cube in cubes
            self.cube_EBO[x] = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.cube_EBO[x])
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube.cube_indices.nbytes, cube.cube_indices, GL_STATIC_DRAW)

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.cube_vertices.itemsize * 8, ctypes.c_void_p(0))

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.cube_vertices.itemsize * 8, ctypes.c_void_p(12))

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cube.cube_vertices.itemsize * 8, ctypes.c_void_p(20))

    def vinculate_quads(self, quads):
        # List that contains the sky and the ground
        self.quad_VAO = [0]*2 
        self.quad_VBO = [0]*2
        self.quad_EBO = [0]*2

        for x, quad in enumerate(quads):
            # Vertex array object for each quad in quads
            self.quad_VAO[x] = glGenVertexArrays(1)
            glBindVertexArray(self.quad_VAO[x])

            # Vertex Buffer Object for each cube in cubes
            self.quad_VBO[x] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.quad_VBO[x])
            glBufferData(GL_ARRAY_BUFFER, quad.quad_vertices.nbytes, quad.quad_vertices, GL_STATIC_DRAW)

            # Quad Element Buffer Object
            self.quad_EBO[x] = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.quad_EBO[x])
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, quad.quad_indices.nbytes, quad.quad_indices, GL_STATIC_DRAW)

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, quad.quad_vertices.itemsize * 8, ctypes.c_void_p(0))

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, quad.quad_vertices.itemsize * 8, ctypes.c_void_p(12))

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, quad.quad_vertices.itemsize * 8, ctypes.c_void_p(20))


# Creating the window
main_window = Window(1080, 720, "Miauzilla")

my_cubes = [0]*(n+m)
for i in range(n+m):
    if i < n:
        my_cubes[i] = Cube()
        my_cubes[i].load_texture(random.randint(0, 1))
        # my_cubes[i].load_texture(0)
    else:
        # Creating the main cubes that are going to be Miauzilla
        my_cubes[i] = Cube()
        my_cubes[i].load_texture(2)

# Creating the ground
ground = Ground()
ground.load_texture(3)

# Creating the sky
sky = Ground()
sky.load_texture(4)

# Initialing the shader
main_shader = Shader()
main_shader.vinculate_cubes(my_cubes)
main_shader.vinculate_quads([ground, sky])

# Using the shader with OpenGL
glUseProgram(main_shader.shader)


glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1080/720, 0.1, 1000)

ground_position = pyrr.Vector3([0.0, 0.0, 0.0])
matrix_ground_position = pyrr.matrix44.create_from_translation(ground_position)

sky_position = pyrr.Vector3([0.0, 9.0, 0.0])
matrix_sky_position = pyrr.matrix44.create_from_translation(sky_position)

# List that stores positions of the cubes
cube_position = [0]*(n+m)
for i in range(n):
    # Initializing the positions of the cubes
    cube_position[i] = pyrr.Vector3([
                        random.randrange(-5.0, 5.0), 1.5, random.randrange(-100, -40)])

for i in range(m):
    # Setting the position of the cat
    cube_position[n+i] = pyrr.Vector3(gato[i])

# Matrix that will control the translation of the cubes
matrix_cube_translation = [0]*(n+m)
for i in range(n+m):
    # Seting the translation matrix to the initial position of the cube
    matrix_cube_translation[i] = pyrr.matrix44.create_from_translation(cube_position[i])

# Default view:
# eye, target, up
# view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 2, 3]), pyrr.Vector3([0, 1.5, 0]), pyrr.Vector3([0, 1, 0]))
view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 2, 3]), pyrr.Vector3([0, 1.5, -1]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(main_shader.shader, "model")
proj_loc = glGetUniformLocation(main_shader.shader, "projection")
view_loc = glGetUniformLocation(main_shader.shader, "view")
# Creating a variable that is going to be used for the position of the light
light_loc = glGetUniformLocation(main_shader.shader, "light_direction")

# Initializing the score:
score = 0

def main():
    global view,score
    translate_cube_z = pyrr.Vector3([0.0, 0.0, 0.1])
    pygame.init()
    music = pygame.mixer.music.load('music/music.mp3')
    pygame.mixer.music.play(-1)
    hitSound = pygame.mixer.Sound('./music/hit.wav')

    glfw.set_input_mode(main_window.win, glfw.STICKY_KEYS, GL_TRUE) 
	# Enable key event callback
    glfw.set_key_callback(main_window.win, main_window.key_event)

    # The main aplication loop
    while glfw.get_key(main_window.win,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(main_window.win):

        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        # Drawing the ground
        model = matrix_ground_position
        glBindVertexArray(main_shader.quad_VAO[0])
        glBindTexture(GL_TEXTURE_2D, ground.id_texture)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawElements(GL_TRIANGLES, len(quad_indices), GL_UNSIGNED_INT, None)

        # Drawing the sky
        model = matrix_sky_position
        glBindVertexArray(main_shader.quad_VAO[1])
        glBindTexture(GL_TEXTURE_2D, sky.id_texture)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawElements(GL_TRIANGLES, len(quad_indices), GL_UNSIGNED_INT, None)

        for i in range(n+m):
            # We will translate every object, except the main character
            if i < n:
                cube_position[i] += translate_cube_z
                if cube_position[i][2] >= 20.0:
                    cube_position[i] = pyrr.Vector3([random.randrange(-5.0, 5.0), 1.5, random.randrange(-100, -40)])
                # Scale the objects that aren't obstacles
                escala = pyrr.matrix44.create_from_scale([1,4,1])
            else:
                # Obtaining the values of the scale previously defined
                escala = pyrr.matrix44.create_from_scale(gato_escala[i-n])
            
            # Calculating the resulting model by multiplying the scale and translation
            model = np.dot(escala, matrix_cube_translation[i])

            glBindVertexArray(main_shader.cube_VAO[i])
            glBindTexture(GL_TEXTURE_2D, my_cubes[i].id_texture)
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)
            matrix_cube_translation[i] = pyrr.matrix44.create_from_translation(cube_position[i])

        for i in range(m):
            for j in range(n):
                # Condition for a crash
                if abs(cube_position[i+n][2] - cube_position[j][2]) < .1 and abs(cube_position[i+n][0] - cube_position[j][0]) < 1:
                    hitSound.play()
                    cube_position[j] = pyrr.Vector3([random.randrange(-5.0, 5.0), 1.5, random.randrange(-100, -40)])
                    score += 1
                    os.system("clear")
                    print("Your actual escore is:",score)

        glfw.swap_buffers(main_window.win)

    # Terminate glfw, free alocated resources
    glfw.terminate()

if __name__ == '__main__':
    main()