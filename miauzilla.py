import ctypes
import random
import sys
from pathlib import Path

import glfw
import numpy as np
import pygame
import pyrr
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


BASE_DIR = Path(__file__).resolve().parent
TEXTURE_PATHS = [
    BASE_DIR / "textures" / "02-obstacle.png",
    BASE_DIR / "textures" / "02-obstacle-2.png",
    BASE_DIR / "textures" / "01-character.png",
    BASE_DIR / "textures" / "03-ground.png",
    BASE_DIR / "textures" / "04-sky.png",
]
BACKGROUND_MUSIC_PATH = BASE_DIR / "music" / "music.mp3"
HIT_SOUND_PATH = BASE_DIR / "music" / "hit.wav"

OBSTACLE_COUNT = 35
CAT_POSITIONS = [
    [0.0, 0.5, -4.5],    # body 1/2
    [0.0, 0.5, -3.5],    # body 2/2
    [0.0, 0.5, -2.5],    # tail 1/3
    [0.0, 0.5, -1.5],    # tail 2/3
    [0.0, 0.5, -0.5],    # tail 3/3
    [0.0, 1.0, -5.0],    # head 1/2
    [0.0, 1.0, -5.5],    # head 2/2
    [0.25, 0.0, -3.25],  # right back leg
    [-0.25, 0.0, -3.25], # left back leg
    [0.25, 0.0, -4.75],  # right front leg
    [-0.25, 0.0, -4.75], # left front leg
]
CAT_SCALES = [
    [1.0, 1.0, 1.0],    # body 1/2
    [1.0, 1.0, 1.0],    # body 2/2
    [0.5, 0.5, 1.0],    # tail 1/3
    [0.3, 0.3, 1.0],    # tail 2/3
    [0.2, 0.2, 1.0],    # tail 3/3
    [1.0, 1.0, 1.0],    # head 1/2
    [0.5, 0.5, 0.5],    # head 2/2
    [0.25, 1.0, 0.25],  # right back leg
    [0.25, 1.0, 0.25],  # left back leg
    [0.25, 1.0, 0.25],  # right front leg
    [0.25, 1.0, 0.25],  # left front leg
]

VERTEX_SHADER_SOURCE = """
#version 330 core

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec3 v_normal;
out vec2 v_texture;

void main() {
    v_normal = normalize((model * vec4(floor(a_normal), 0.0)).xyz);
    v_texture = a_texture;
    gl_Position = projection * view * model * vec4(a_position, 1.0);
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core

in vec2 v_texture;
in vec3 v_normal;

out vec4 out_texture;

uniform vec3 light_direction;
uniform sampler2D s_texture;

void main() {
    float diffuse = max(dot(v_normal, light_direction), 0.0);
    float ambient = 0.3;
    float lighting = max(diffuse, ambient);

    vec4 sample1 = texture(s_texture, v_texture);
    out_texture = vec4(sample1.xyz * lighting, sample1.a);
}
"""

QUAD_VERTICES = [
    # Vertices               # Texture      # Light
    -10.0, -0.5, 20.0,       0.0, 0.0,      0.0, 1.0, 0.0,
    10.0, -0.5, 20.0,        1.0, 0.0,      0.0, 1.0, 0.0,
    10.0, -0.5, -10000.0,    1.0, 1.0,      0.0, 1.0, 0.0,
    -10.0, -0.5, -10000.0,   0.0, 1.0,      0.0, 1.0, 0.0,
]

QUAD_INDICES = [0, 1, 2, 2, 3, 0]

CUBE_VERTICES = [
    # Vertices            # Texture    # Light
    -0.5, -0.5, 0.5,      0.0, 0.0,    0.0, 0.0, 1.0,
    0.5, -0.5, 0.5,       1.0, 0.0,    0.0, 0.0, 1.0,
    0.5, 0.5, 0.5,        1.0, 1.0,    0.0, 0.0, 1.0,
    -0.5, 0.5, 0.5,       0.0, 1.0,    0.0, 0.0, 1.0,

    -0.5, -0.5, -0.5,     0.0, 0.0,    0.0, 0.0, -1.0,
    0.5, -0.5, -0.5,      1.0, 0.0,    0.0, 0.0, -1.0,
    0.5, 0.5, -0.5,       1.0, 1.0,    0.0, 0.0, -1.0,
    -0.5, 0.5, -0.5,      0.0, 1.0,    0.0, 0.0, -1.0,

    0.5, -0.5, -0.5,      0.0, 0.0,    1.0, 0.0, -1.0,
    0.5, 0.5, -0.5,       1.0, 0.0,    1.0, 0.0, -1.0,
    0.5, 0.5, 0.5,        1.0, 1.0,    1.0, 0.0, -1.0,
    0.5, -0.5, 0.5,       0.0, 1.0,    1.0, 0.0, -1.0,

    -0.5, 0.5, -0.5,      0.0, 0.0,   -1.0, 0.0, 0.0,
    -0.5, -0.5, -0.5,     1.0, 0.0,   -1.0, 0.0, 0.0,
    -0.5, -0.5, 0.5,      1.0, 1.0,   -1.0, 0.0, 0.0,
    -0.5, 0.5, 0.5,       0.0, 1.0,   -1.0, 0.0, 0.0,

    -0.5, -0.5, -0.5,     0.0, 0.0,    0.0, -1.0, -1.0,
    0.5, -0.5, -0.5,      1.0, 0.0,    0.0, -1.0, -1.0,
    0.5, -0.5, 0.5,       1.0, 1.0,    0.0, -1.0, -1.0,
    -0.5, -0.5, 0.5,      0.0, 1.0,    0.0, -1.0, -1.0,

    0.5, 0.5, -0.5,       0.0, 0.0,    0.0, 1.0, -1.0,
    -0.5, 0.5, -0.5,      1.0, 0.0,    0.0, 1.0, -1.0,
    -0.5, 0.5, 0.5,       1.0, 1.0,    0.0, 1.0, -1.0,
    0.5, 0.5, 0.5,        0.0, 1.0,    0.0, 1.0, -1.0,
]

CUBE_INDICES = [
    0,
    1,
    2,
    2,
    3,
    0,
    4,
    5,
    6,
    6,
    7,
    4,
    8,
    9,
    10,
    10,
    11,
    8,
    12,
    13,
    14,
    14,
    15,
    12,
    16,
    17,
    18,
    18,
    19,
    16,
    20,
    21,
    22,
    22,
    23,
    20,
]


def load_texture_assets():
    texture_surfaces = []
    texture_data = []

    for texture_path in TEXTURE_PATHS:
        texture_surface = Image.open(texture_path).transpose(Image.FLIP_TOP_BOTTOM)
        texture_surfaces.append(texture_surface)
        texture_data.append(texture_surface.convert("RGBA").tobytes())

    return texture_surfaces, texture_data


def random_spawn_position():
    return pyrr.Vector3(
        [float(random.randint(-5, 4)), 1.5, float(random.randint(-100, -41))]
    )


class Cube:
    def __init__(self):
        self.cube_vertices = np.array(CUBE_VERTICES, dtype=np.float32)
        self.cube_indices = np.array(CUBE_INDICES, dtype=np.uint32)
        self.id_texture = 0

    def load_texture(self, texture_surface, texture_bytes):
        self.id_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            texture_surface.width,
            texture_surface.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            texture_bytes,
        )
        glGenerateMipmap(GL_TEXTURE_2D)


class Ground:
    def __init__(self):
        self.quad_vertices = np.array(QUAD_VERTICES, dtype=np.float32)
        self.quad_indices = np.array(QUAD_INDICES, dtype=np.uint32)
        self.id_texture = 0

    def load_texture(self, texture_surface, texture_bytes):
        self.id_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            texture_surface.width,
            texture_surface.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            texture_bytes,
        )
        glGenerateMipmap(GL_TEXTURE_2D)


class Window:
    def __init__(self, width, height, title, game):
        if not glfw.init():
            raise RuntimeError("glfw could not be initialized")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.game = game
        self.win = glfw.create_window(width, height, title, None, None)
        self.mode_perspective = 0
        self.light_perspective = 0

        if not self.win:
            glfw.terminate()
            raise RuntimeError("glfw window could not be created")

        glfw.make_context_current(self.win)
        glfw.set_window_size_callback(self.win, self.window_resize)
        glfw.set_key_callback(self.win, self.key_event)

    def window_resize(self, window, width, height):
        if height == 0:
            return

        glViewport(0, 0, width, height)

        if self.game.proj_loc is None:
            return

        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45, width / height, 0.1, 1000
        )
        glUseProgram(self.game.shader.shader)
        glUniformMatrix4fv(self.game.proj_loc, 1, GL_FALSE, projection)

    def key_event(self, window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return

        if key == glfw.KEY_Q:
            self.game.cycle_camera()
        elif key == glfw.KEY_E:
            self.game.cycle_light()
        elif key in (glfw.KEY_A, glfw.KEY_LEFT):
            self.game.move_cat(-0.5, 0.0)
        elif key in (glfw.KEY_D, glfw.KEY_RIGHT):
            self.game.move_cat(0.5, 0.0)
        elif key in (glfw.KEY_S, glfw.KEY_DOWN):
            self.game.move_cat(0.0, 0.5)
        elif key in (glfw.KEY_W, glfw.KEY_UP):
            self.game.move_cat(0.0, -0.5)


class Shader:
    def __init__(self):
        self.shader = compileProgram(
            compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER),
        )

    def vinculate_cubes(self, cubes):
        self.cube_VAO = [0] * len(cubes)
        self.cube_VBO = [0] * len(cubes)
        self.cube_EBO = [0] * len(cubes)

        for index, cube in enumerate(cubes):
            self.cube_VAO[index] = glGenVertexArrays(1)
            glBindVertexArray(self.cube_VAO[index])

            self.cube_VBO[index] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.cube_VBO[index])
            glBufferData(
                GL_ARRAY_BUFFER, cube.cube_vertices.nbytes, cube.cube_vertices, GL_STATIC_DRAW
            )

            self.cube_EBO[index] = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.cube_EBO[index])
            glBufferData(
                GL_ELEMENT_ARRAY_BUFFER,
                cube.cube_indices.nbytes,
                cube.cube_indices,
                GL_STATIC_DRAW,
            )

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(
                0, 3, GL_FLOAT, GL_FALSE, cube.cube_vertices.itemsize * 8, ctypes.c_void_p(0)
            )

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(
                1, 2, GL_FLOAT, GL_FALSE, cube.cube_vertices.itemsize * 8, ctypes.c_void_p(12)
            )

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(
                2, 3, GL_FLOAT, GL_FALSE, cube.cube_vertices.itemsize * 8, ctypes.c_void_p(20)
            )

    def vinculate_quads(self, quads):
        self.quad_VAO = [0] * len(quads)
        self.quad_VBO = [0] * len(quads)
        self.quad_EBO = [0] * len(quads)

        for index, quad in enumerate(quads):
            self.quad_VAO[index] = glGenVertexArrays(1)
            glBindVertexArray(self.quad_VAO[index])

            self.quad_VBO[index] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.quad_VBO[index])
            glBufferData(
                GL_ARRAY_BUFFER, quad.quad_vertices.nbytes, quad.quad_vertices, GL_STATIC_DRAW
            )

            self.quad_EBO[index] = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.quad_EBO[index])
            glBufferData(
                GL_ELEMENT_ARRAY_BUFFER,
                quad.quad_indices.nbytes,
                quad.quad_indices,
                GL_STATIC_DRAW,
            )

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(
                0, 3, GL_FLOAT, GL_FALSE, quad.quad_vertices.itemsize * 8, ctypes.c_void_p(0)
            )

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(
                1, 2, GL_FLOAT, GL_FALSE, quad.quad_vertices.itemsize * 8, ctypes.c_void_p(12)
            )

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(
                2, 3, GL_FLOAT, GL_FALSE, quad.quad_vertices.itemsize * 8, ctypes.c_void_p(20)
            )


class Game:
    def __init__(self):
        self.proj_loc = None
        self.model_loc = None
        self.view_loc = None
        self.light_loc = None
        self.texture_surfaces, self.texture_data = load_texture_assets()
        self.window = Window(1080, 720, "Miauzilla", self)
        self.obstacle_count = OBSTACLE_COUNT
        self.cat_count = len(CAT_POSITIONS)
        self.score = 0
        self.hit_sound = None
        self.background_music = None
        self.background_music_channel = None
        self.audio_enabled = False
        self.view = pyrr.matrix44.create_look_at(
            pyrr.Vector3([0, 2, 3]),
            pyrr.Vector3([0, 1.5, -1]),
            pyrr.Vector3([0, 1, 0]),
        )
        self.translate_cube_z = pyrr.Vector3([0.0, 0.0, 0.1])

        self._create_scene()
        self._init_audio()

    def _texture(self, index):
        return self.texture_surfaces[index], self.texture_data[index]

    def _reset_obstacle_position(self, index):
        self.cube_position[index] = random_spawn_position()
        self.matrix_cube_translation[index] = pyrr.matrix44.create_from_translation(
            self.cube_position[index]
        )

    def _create_scene(self):
        self.my_cubes = []
        for _ in range(self.obstacle_count):
            cube = Cube()
            cube.load_texture(*self._texture(random.randint(0, 1)))
            self.my_cubes.append(cube)

        for _ in range(self.cat_count):
            cube = Cube()
            cube.load_texture(*self._texture(2))
            self.my_cubes.append(cube)

        self.ground = Ground()
        self.ground.load_texture(*self._texture(3))

        self.sky = Ground()
        self.sky.load_texture(*self._texture(4))

        self.shader = Shader()
        self.shader.vinculate_cubes(self.my_cubes)
        self.shader.vinculate_quads([self.ground, self.sky])

        glUseProgram(self.shader.shader)
        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.ground_position = pyrr.Vector3([0.0, 0.0, 0.0])
        self.matrix_ground_position = pyrr.matrix44.create_from_translation(self.ground_position)
        self.sky_position = pyrr.Vector3([0.0, 9.0, 0.0])
        self.matrix_sky_position = pyrr.matrix44.create_from_translation(self.sky_position)

        self.cube_position = [random_spawn_position() for _ in range(self.obstacle_count)]
        self.cube_position.extend(pyrr.Vector3(position) for position in CAT_POSITIONS)
        self.matrix_cube_translation = [
            pyrr.matrix44.create_from_translation(position) for position in self.cube_position
        ]

        self.model_loc = glGetUniformLocation(self.shader.shader, "model")
        self.proj_loc = glGetUniformLocation(self.shader.shader, "projection")
        self.view_loc = glGetUniformLocation(self.shader.shader, "view")
        self.light_loc = glGetUniformLocation(self.shader.shader, "light_direction")

        framebuffer_width, framebuffer_height = glfw.get_framebuffer_size(self.window.win)
        glViewport(0, 0, framebuffer_width, framebuffer_height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45, framebuffer_width / framebuffer_height, 0.1, 1000
        )
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)
        glUniform3f(self.light_loc, 0.0, 0.0, 1.0)

    def _init_audio(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

        try:
            pygame.mixer.init()
        except pygame.error as error:
            print(f"Audio disabled: {error}", file=sys.stderr)
            return

        try:
            pygame.mixer.music.load(BACKGROUND_MUSIC_PATH.as_posix())
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
            self.audio_enabled = True
        except pygame.error as music_error:
            try:
                self.background_music = pygame.mixer.Sound(BACKGROUND_MUSIC_PATH.as_posix())
                self.background_music.set_volume(1.0)
                self.background_music_channel = self.background_music.play(loops=-1)
                self.audio_enabled = True
            except pygame.error as fallback_error:
                print(
                    "Background music disabled: "
                    f"{music_error}. Fallback also failed: {fallback_error}",
                    file=sys.stderr,
                )

        try:
            self.hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH.as_posix())
            self.hit_sound.set_volume(1.0)
            self.audio_enabled = True
        except pygame.error as error:
            print(f"Hit sound disabled: {error}", file=sys.stderr)

    def cycle_camera(self):
        if self.window.mode_perspective == 0:
            self.view = pyrr.matrix44.create_look_at(
                pyrr.Vector3([10, 8, 3]),
                pyrr.Vector3([0, 1.5, 0]),
                pyrr.Vector3([0, 1, 0]),
            )
            self.window.mode_perspective = 1
        elif self.window.mode_perspective == 1:
            self.view = pyrr.matrix44.create_look_at(
                pyrr.Vector3([-10, 8, 3]),
                pyrr.Vector3([0, 1.5, 0]),
                pyrr.Vector3([0, 1, 0]),
            )
            self.window.mode_perspective = 2
        else:
            self.view = pyrr.matrix44.create_look_at(
                pyrr.Vector3([0, 2, 3]),
                pyrr.Vector3([0, 1.5, -1]),
                pyrr.Vector3([0, 1, 0]),
            )
            self.window.mode_perspective = 0

    def cycle_light(self):
        if self.window.light_perspective == 0:
            glUniform3f(self.light_loc, 0.0, 0.0, 1.0)
            self.window.light_perspective = 1
        elif self.window.light_perspective == 1:
            glUniform3f(self.light_loc, 0.0, 1.0, 0.0)
            self.window.light_perspective = 2
        else:
            glUniform3f(self.light_loc, 1.0, 0.0, 0.0)
            self.window.light_perspective = 0

    def move_cat(self, delta_x, delta_z):
        translation = pyrr.Vector3([delta_x, 0.0, delta_z])
        for index in range(self.obstacle_count, self.obstacle_count + self.cat_count):
            self.cube_position[index] += translation

    def _draw_quad(self, vao, texture_id, model_matrix):
        glBindVertexArray(vao)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model_matrix)
        glDrawElements(GL_TRIANGLES, len(QUAD_INDICES), GL_UNSIGNED_INT, None)

    def _draw_cube(self, index, model_matrix):
        glBindVertexArray(self.shader.cube_VAO[index])
        glBindTexture(GL_TEXTURE_2D, self.my_cubes[index].id_texture)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model_matrix)
        glDrawElements(GL_TRIANGLES, len(CUBE_INDICES), GL_UNSIGNED_INT, None)

    def _update_obstacles(self):
        for index in range(self.obstacle_count):
            self.cube_position[index] += self.translate_cube_z
            if self.cube_position[index][2] >= 20.0:
                self._reset_obstacle_position(index)

    def _draw_scene(self):
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, self.view)
        self._draw_quad(self.shader.quad_VAO[0], self.ground.id_texture, self.matrix_ground_position)
        self._draw_quad(self.shader.quad_VAO[1], self.sky.id_texture, self.matrix_sky_position)

        for index in range(self.obstacle_count + self.cat_count):
            if index < self.obstacle_count:
                scale = pyrr.matrix44.create_from_scale([1, 4, 1])
            else:
                scale = pyrr.matrix44.create_from_scale(CAT_SCALES[index - self.obstacle_count])

            self.matrix_cube_translation[index] = pyrr.matrix44.create_from_translation(
                self.cube_position[index]
            )
            model = np.dot(scale, self.matrix_cube_translation[index])
            self._draw_cube(index, model)

    def _detect_collisions(self):
        for cat_index in range(self.cat_count):
            for obstacle_index in range(self.obstacle_count):
                cat_position = self.cube_position[self.obstacle_count + cat_index]
                obstacle_position = self.cube_position[obstacle_index]

                if (
                    abs(cat_position[2] - obstacle_position[2]) < 0.1
                    and abs(cat_position[0] - obstacle_position[0]) < 1
                ):
                    if self.hit_sound is not None:
                        self.hit_sound.play()
                    self._reset_obstacle_position(obstacle_index)
                    self.score += 1
                    print(f"Your actual score is: {self.score}")

    def run(self):
        glfw.set_input_mode(self.window.win, glfw.STICKY_KEYS, GL_TRUE)

        try:
            while (
                glfw.get_key(self.window.win, glfw.KEY_ESCAPE) != glfw.PRESS
                and not glfw.window_should_close(self.window.win)
            ):
                glfw.poll_events()
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                self._update_obstacles()
                self._draw_scene()
                self._detect_collisions()

                glfw.swap_buffers(self.window.win)
        finally:
            if self.audio_enabled:
                pygame.mixer.music.stop()
                if self.background_music_channel is not None:
                    self.background_music_channel.stop()
            pygame.quit()
            glfw.terminate()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
