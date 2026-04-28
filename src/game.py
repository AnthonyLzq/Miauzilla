import glfw
import numpy as np
import pyrr
from OpenGL.GL import (
    GL_BLEND,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_FALSE,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_SRC_ALPHA,
    GL_TEXTURE_2D,
    GL_TRIANGLES,
    GL_TRUE,
    GL_UNSIGNED_INT,
    glBindTexture,
    glBindVertexArray,
    glBlendFunc,
    glClear,
    glClearColor,
    glDrawElements,
    glEnable,
    glGetUniformLocation,
    glUniform3f,
    glUniformMatrix4fv,
    glUseProgram,
    glViewport,
)

from .assets import load_texture_assets, random_spawn_position
from .audio import AudioManager
from .config import (
    CAT_POSITIONS,
    CAT_SCALES,
    OBSTACLE_COUNT,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)
from .geometry import CUBE_INDICES, QUAD_INDICES
from .rendering import Cube, Ground, Shader
from .window import Window


class Game:
    def __init__(self):
        self.projection_uniform_location = None
        self.model_uniform_location = None
        self.view_uniform_location = None
        self.light_direction_uniform_location = None
        self.texture_surfaces, self.texture_data = load_texture_assets()
        self.obstacle_count = OBSTACLE_COUNT
        self.cat_count = len(CAT_POSITIONS)
        self.score = 0
        self.view = pyrr.matrix44.create_look_at(
            pyrr.Vector3([0, 2, 3]),
            pyrr.Vector3([0, 1.5, -1]),
            pyrr.Vector3([0, 1, 0]),
        )
        self.translate_cube_z = pyrr.Vector3([0.0, 0.0, 0.1])
        self.audio = AudioManager()
        self.window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, self)

        self._create_scene()
        self.audio.initialize()

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
            cube.load_texture(*self._texture(np.random.randint(0, 2)))
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
        self.shader.bind_cubes(self.my_cubes)
        self.shader.bind_quads([self.ground, self.sky])

        glUseProgram(self.shader.program)
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

        self.model_uniform_location = glGetUniformLocation(self.shader.program, "model")
        self.projection_uniform_location = glGetUniformLocation(self.shader.program, "projection")
        self.view_uniform_location = glGetUniformLocation(self.shader.program, "view")
        self.light_direction_uniform_location = glGetUniformLocation(
            self.shader.program, "light_direction"
        )

        framebuffer_width, framebuffer_height = glfw.get_framebuffer_size(self.window.win)
        glViewport(0, 0, framebuffer_width, framebuffer_height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45, framebuffer_width / framebuffer_height, 0.1, 1000
        )
        glUniformMatrix4fv(self.projection_uniform_location, 1, GL_FALSE, projection)
        glUniform3f(self.light_direction_uniform_location, 0.0, 0.0, 1.0)

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
            glUniform3f(self.light_direction_uniform_location, 0.0, 0.0, 1.0)
            self.window.light_perspective = 1
        elif self.window.light_perspective == 1:
            glUniform3f(self.light_direction_uniform_location, 0.0, 1.0, 0.0)
            self.window.light_perspective = 2
        else:
            glUniform3f(self.light_direction_uniform_location, 1.0, 0.0, 0.0)
            self.window.light_perspective = 0

    def move_cat(self, delta_x, delta_z):
        translation = pyrr.Vector3([delta_x, 0.0, delta_z])
        for index in range(self.obstacle_count, self.obstacle_count + self.cat_count):
            self.cube_position[index] += translation

    def _draw_quad(self, vao, texture_id, model_matrix):
        glBindVertexArray(vao)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glUniformMatrix4fv(self.model_uniform_location, 1, GL_FALSE, model_matrix)
        glDrawElements(GL_TRIANGLES, len(QUAD_INDICES), GL_UNSIGNED_INT, None)

    def _draw_cube(self, index, model_matrix):
        glBindVertexArray(self.shader.cube_vertex_array_objects[index])
        glBindTexture(GL_TEXTURE_2D, self.my_cubes[index].texture_id)
        glUniformMatrix4fv(self.model_uniform_location, 1, GL_FALSE, model_matrix)
        glDrawElements(GL_TRIANGLES, len(CUBE_INDICES), GL_UNSIGNED_INT, None)

    def _update_obstacles(self):
        for index in range(self.obstacle_count):
            self.cube_position[index] += self.translate_cube_z
            if self.cube_position[index][2] >= 20.0:
                self._reset_obstacle_position(index)

    def _draw_scene(self):
        glUniformMatrix4fv(self.view_uniform_location, 1, GL_FALSE, self.view)
        self._draw_quad(
            self.shader.quad_vertex_array_objects[0],
            self.ground.texture_id,
            self.matrix_ground_position,
        )
        self._draw_quad(
            self.shader.quad_vertex_array_objects[1],
            self.sky.texture_id,
            self.matrix_sky_position,
        )

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
                    self.audio.play_hit()
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
            self.audio.shutdown()
            glfw.terminate()


def main():
    game = Game()
    game.run()
