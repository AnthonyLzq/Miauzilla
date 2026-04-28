import glfw
import pyrr
from OpenGL.GL import GL_FALSE, glUniformMatrix4fv, glUseProgram, glViewport


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

        if self.game.projection_uniform_location is None:
            return

        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45, width / height, 0.1, 1000
        )
        glUseProgram(self.game.shader.program)
        glUniformMatrix4fv(self.game.projection_uniform_location, 1, GL_FALSE, projection)

    def key_event(self, window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return

        if key == glfw.KEY_Q:
            self.game.cycle_camera()
        elif key == glfw.KEY_E:
            self.game.cycle_light()
