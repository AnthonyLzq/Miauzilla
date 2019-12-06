import glfw
from math import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
import random
from PIL import Image
import os

# Esta variable realiza el manejo de la posición y la textura de cualquier objeto gráfico que sea creado con el shader program
vertex_src = """
#version 310 es

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;

uniform mat4 model; //translation
uniform mat4 projection;
uniform mat4 view;

//out vec3 v_color;
out vec2 v_texture;

void main(){
    gl_Position = projection * view *model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

# Esta variable "encapsula" la textura (imagen) que se desea usar con el tipo de textura a usar (2D en este caso), y retorna una textura 2D con la textura (imagen) deseada.
fragment_src = """
#version 310 es

precision mediump float;

in vec2 v_texture; 

out vec4 out_texture;

uniform sampler2D s_texture;

void main(){
    out_texture = texture(s_texture, v_texture);
}
"""

quad_vertices = [#Vertices                #Texture
                -10.0, -0.5,  20.0,      0.0, 0.0,
                 10.0, -0.5,  20.0,      1.0, 0.0,
                 10.0, -0.5,  -10000,    1.0, 1.0,
                -10.0, -0.5,  -10000,    0.0, 1.0]


quad_indices = [0, 1, 2, 2, 3, 0]


cube_vertices = [#Vertices         #Texture
                -0.5, -0.5,  0.5,  0.0, 0.0,
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
            

cube_indices =  [0,  1,  2,  2,  3,  0,
                4,  5,  6,  6,  7,  4,
                8,  9, 10, 10, 11,  8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]

# List that stores textures
texture_surface = [  
                Image.open('./textures/cat.png'), 
                Image.open('./textures/ursa.png'),
                Image.open('./textures/01-character.png'),
                Image.open('./textures/03-ground.png')]

# Seteando cantidad de cubos obstaculos
n = 3

# Seteando las pos del los cubos que conforman el gato
gato = [[0, 0.5, -4.5], #cuerpo1/2
        [0, 0.5, -3.5], #cuerpo2/2 
        [0, 0.5, -2.5], #cola1/3
        [0, 0.5, -1.5], #cola2/3
        [0, 0.5, -0.5], #cola2/3
        [0.0, 1.0, -5.0], #cabeza1/2
        [0, 1, -5.5], #cabeza2/2    
        [0.25, 0, -3.25], #pierna trasera derecha
        [-0.25, 0, -3.25], #pierna trasera izquierda
        [0.25, 0, -4.75], #pierna delantera derecha
        [-0.25, 0, -4.75] #pierna delantera izquierda
] #Fin de las pos de los cubos

gato_escala = [
                [1, 1, 1], #cuerpo1/2
                [1, 1, 1], #cuerpo2/2
                [0.5, 0.5, 1], #cola1/3
                [0.3, 0.3, 1], #cola2/3
                [0.2, 0.2, 1], #cola2/3
                [1, 1, 1], #cabeza1/2
                [0.5, 0.5, 0.5], #cabeza2/2
                [0.25, 1, 0.25], #pierna trasera derecha
                [0.25, 1, 0.25], #pierna trasera izquierda
                [0.25, 1, 0.25], #pierna delantera derecha
                [0.25, 1, 0.25] #pierna delantera izquierda
] #Fin de las pos de los cubos

# Seteando cantidad de cubos que conformar el gato principal
m = len(gato)

# Reversing the images to be properly render
for i in range(len(texture_surface)):
    texture_surface[i] = texture_surface[i].transpose(Image.FLIP_TOP_BOTTOM)

texture_data = [0]*len(texture_surface)
for i in range(len(texture_data)):
    texture_data[i] = texture_surface[i].convert("RGBA").tobytes()

class Cube:
    '''
    Esta clase es la que representará los cubos que serán renderizados en la ventana principal.
    Se inician los vértices modificando la constante 'cube_vertices' e 'cube_indices' que se encuentran líneas arriba, pasando estas a numpys array.
    
    Esta clase contiene los siguientes métodos:
        - load_texture: se encarga de envolver al cubo con una textura pasada como parámetro.
    '''
    def __init__(self):
        # Conversión de array a np array, para los vértices e índices.
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

    Esta clase contiene los siguientes métodos:
    - load_texture: se encarga de envolver al cuadrado con una textura pasada como parámetro.

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
        # glEnable(GL_TEXTURE_2D)


class Window:
    '''
    Esta clase es la que representa la ventana principal donde el juego toma lugar, se inicializa recibiendo como parámetros un ancho, largo y un título.
    La ventana se crea por defecto en la posición (400, 200).
    
    Esta clase contiene los siguientes métodos:
        - window_resize: es la callback que se ejecuta siempre que haya un evento de resize de ventana.
    '''
    def __init__(self, width: int, height: int, title: str):
        if not glfw.init():
            raise Exception("glfw can not be initilized")

        self.win = glfw.create_window(width, height, title, None, None)
        self.mode_perspective = 0

        if not self.win:
            glfw.terminate()
            raise Exception("glfw can not be created!")

        glfw.set_window_pos(self.win, 400, 200)
        glfw.make_context_current(self.win)
        glfw.set_window_size_callback(self.win, self.window_resize)

    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, 1000)
        # translation = pyrr.matrix44.create_from_translation([0.0, 0.1, 0.0])
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    def key_event(self, window, key, scancode, action, mods):
        global view, n, m, cube_position

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

        if action == glfw.PRESS and key == glfw.KEY_A:
            translate_cube_x = pyrr.Vector3([-0.5, 0.0, 0.0])
            for i in range(m):
                cube_position[n+i] += translate_cube_x
        elif action == glfw.PRESS and key == glfw.KEY_D:
            translate_cube_x = pyrr.Vector3([+0.5, 0.0, 0.0])
            for i in range(m):
                cube_position[n+i] += translate_cube_x



class Shader:
    '''
    Esta clase representará al shader que utilizará el programa para renderizar los objetos OpenGl. Este se inicializa recibiendo como parámetro el vector que almacena los cubos a renderizar.

    Esta clase contiene los siguientes métodos:
        - vinculate_cubes: asocia a cada cubo de una lista de cubos data un VAO, VBO y EBO.
        - vinculate_quads: asocia el suelo con un VAO, VBO y EBO.
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
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.cube_vertices.itemsize * 5, ctypes.c_void_p(0))

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.cube_vertices.itemsize * 5, ctypes.c_void_p(12))

            # glBindVertexArray(0)
    
    def vinculate_quads(self, quad):
        # Quad VAO
        self.quad_VAO = glGenVertexArrays(1)
        glBindVertexArray(self.quad_VAO)

        # Quad Vertex Buffer Object
        self.quad_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.quad_VBO)
        glBufferData(GL_ARRAY_BUFFER, quad.quad_vertices.nbytes, quad.quad_vertices, GL_STATIC_DRAW)

        # Quad Element Buffer Object
        self.quad_EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.quad_EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, quad.quad_indices.nbytes, quad.quad_indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, quad.quad_vertices.itemsize * 5, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, quad.quad_vertices.itemsize * 5, ctypes.c_void_p(12))

        # glBindVertexArray(0)

# Creating the window
main_window = Window(1080, 720, "Miauzilla")

my_cubes = [0]*(n+m)
for i in range(n+m):
    if i < n:
        my_cubes[i] = Cube()
        my_cubes[i].load_texture(random.randint(0, 1))
    else:
        # Creando el cubo principal que será el gato
        my_cubes[i] = Cube()
        my_cubes[i].load_texture(2)

# Creando el suelo
ground = Ground()
ground.load_texture(3)

# Iniciando los Shaders de my_cubes
main_shader = Shader()
main_shader.vinculate_cubes(my_cubes)
main_shader.vinculate_quads(ground)


glUseProgram(main_shader.shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1080/720, 0.1, 1000)

ground_position = pyrr.Vector3([0.0, 0.0, 0.0])
matrix_ground_position = pyrr.matrix44.create_from_translation(ground_position)

# List that stores positions of the cubes
cube_position = [0]*(n+m)
for i in range(n):
    # Initializing the positions of the cubes
    cube_position[i] = pyrr.Vector3([
                        random.randrange(-5.0, 5.0), 1.5, random.randrange(-100, -40)])

for i in range(m):
    # Seteando las posicion del gato principal
    cube_position[n+i] = pyrr.Vector3(gato[i])

# Matrix that will control the translation of the cubes
matrix_cube_translation = [0]*(n+m)
for i in range(n+m):
    # Seting the translation matrix to the initial position of the cube
    matrix_cube_translation[i] = pyrr.matrix44.create_from_translation(cube_position[i])

# eye, target, up
# view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 2, 3]), pyrr.Vector3([0, 1.5, 0]), pyrr.Vector3([0, 1, 0]))
view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 2, 3]), pyrr.Vector3([0, 1.5, -1]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(main_shader.shader, "model")
proj_loc = glGetUniformLocation(main_shader.shader, "projection")
view_loc = glGetUniformLocation(main_shader.shader, "view")

# glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
# glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

#Iniciando el puntaje:
puntaje = 0
def main():
    global view,puntaje
    translate_cube_z = pyrr.Vector3([0.0, 0.0, 0.1])
    
    glfw.set_input_mode(main_window.win, glfw.STICKY_KEYS,GL_TRUE) 
	# Enable key event callback
    glfw.set_key_callback(main_window.win, main_window.key_event)

    # The main aplication loop
    while glfw.get_key(main_window.win,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(main_window.win):

        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        # Drawing the ground
        model = matrix_ground_position
        glBindVertexArray(main_shader.quad_VAO)
        glBindTexture(GL_TEXTURE_2D, ground.id_texture)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawElements(GL_TRIANGLES, len(quad_indices), GL_UNSIGNED_INT, None)

        for i in range(n+m):
            # We will translate every object, except the main character
            if i < n:
                cube_position[i] += translate_cube_z
                if cube_position[i][2] >= 0.0:
                    cube_position[i] = pyrr.Vector3([random.randrange(-5.0, 5.0), 1.5, random.randrange(-100, -40)])
                #Escala de todos los objetos que son obstaculos
                escala = pyrr.matrix44.create_from_scale([1,4,1])
            else:
                #Obteniendo los valores de la escala previamente difinida
                escala = pyrr.matrix44.create_from_scale(gato_escala[i-n])
            
            #Hallando el model resultante al multiplicar la escala y la translacion
            model = np.dot(escala,matrix_cube_translation[i])

            glBindVertexArray(main_shader.cube_VAO[i])
            glBindTexture(GL_TEXTURE_2D, my_cubes[i].id_texture)
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)
            matrix_cube_translation[i] = pyrr.matrix44.create_from_translation(cube_position[i])
        for i in range(m):
            for j in range(n):
                #Condicion para que exista un choque
                if abs(cube_position[i+n][2] - cube_position[j][2]) < .1 and abs(cube_position[i+n][0] - cube_position[j][0]) < 1:
                    cube_position[j] = pyrr.Vector3([random.randrange(-5.0, 5.0), 1.5, random.randrange(-100, -40)])
                    puntaje+=1
                    os.system("clear")
                    print("Tu puntaje actual es: ",puntaje)

        glfw.swap_buffers(main_window.win)

    # Terminate glfw, free alocated resources
    glfw.terminate()

if __name__ == '__main__':
    main()