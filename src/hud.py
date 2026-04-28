import ctypes

import numpy as np
import pygame
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_CLAMP_TO_EDGE,
    GL_DYNAMIC_DRAW,
    GL_ELEMENT_ARRAY_BUFFER,
    GL_FALSE,
    GL_FLOAT,
    GL_FRAGMENT_SHADER,
    GL_LINEAR,
    GL_RGBA,
    GL_STATIC_DRAW,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_TRIANGLES,
    GL_UNSIGNED_BYTE,
    GL_UNSIGNED_INT,
    GL_VERTEX_SHADER,
    glBindBuffer,
    glBindTexture,
    glBindVertexArray,
    glBufferData,
    glDeleteBuffers,
    glDeleteProgram,
    glDeleteTextures,
    glDeleteVertexArrays,
    glDrawElements,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenTextures,
    glGenVertexArrays,
    glGetUniformLocation,
    glTexImage2D,
    glTexParameteri,
    glUniform1i,
    glUseProgram,
    glVertexAttribPointer,
)
from OpenGL.GL.shaders import compileProgram, compileShader

from .config import HUD_FONT_SIZE, HUD_MARGIN, HUD_TEXT_COLOR


HUD_VERTEX_SHADER_SOURCE = """
#version 330 core

layout(location = 0) in vec2 a_position;
layout(location = 1) in vec2 a_texture;

out vec2 v_texture;

void main() {
    v_texture = a_texture;
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""

HUD_FRAGMENT_SHADER_SOURCE = """
#version 330 core

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D hud_texture;

void main() {
    out_color = texture(hud_texture, v_texture);
}
"""


class ScoreHud:
    def __init__(self):
        if not pygame.font.get_init():
            pygame.font.init()

        self.font = pygame.font.Font(None, HUD_FONT_SIZE)
        self.program = compileProgram(
            compileShader(HUD_VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER),
            compileShader(HUD_FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER),
        )
        self.vertex_array_object = glGenVertexArrays(1)
        self.vertex_buffer = glGenBuffers(1)
        self.element_buffer = glGenBuffers(1)
        self.texture_id = glGenTextures(1)
        self.indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        self.cached_score = None
        self.cached_framebuffer_size = None

        glBindVertexArray(self.vertex_array_object)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, 4 * 4 * 4, None, GL_DYNAMIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            self.indices.nbytes,
            self.indices,
            GL_STATIC_DRAW,
        )

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(8))

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glUseProgram(self.program)
        glUniform1i(glGetUniformLocation(self.program, "hud_texture"), 0)

    def _update_texture(self, score, framebuffer_width, framebuffer_height):
        score_surface = self.font.render(f"Score: {score}", True, HUD_TEXT_COLOR)
        score_surface = pygame.transform.flip(score_surface, False, True)
        score_width, score_height = score_surface.get_size()
        texture_bytes = pygame.image.tobytes(score_surface, "RGBA", False)

        left = HUD_MARGIN
        top = HUD_MARGIN
        right = left + score_width
        bottom = top + score_height

        left_ndc = (left / framebuffer_width) * 2.0 - 1.0
        right_ndc = (right / framebuffer_width) * 2.0 - 1.0
        top_ndc = 1.0 - (top / framebuffer_height) * 2.0
        bottom_ndc = 1.0 - (bottom / framebuffer_height) * 2.0

        vertices = np.array(
            [
                left_ndc,
                top_ndc,
                0.0,
                1.0,
                right_ndc,
                top_ndc,
                1.0,
                1.0,
                right_ndc,
                bottom_ndc,
                1.0,
                0.0,
                left_ndc,
                bottom_ndc,
                0.0,
                0.0,
            ],
            dtype=np.float32,
        )

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            score_width,
            score_height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            texture_bytes,
        )

        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)

        self.cached_score = score
        self.cached_framebuffer_size = (framebuffer_width, framebuffer_height)

    def render(self, score, framebuffer_width, framebuffer_height):
        if self.cached_score != score or self.cached_framebuffer_size != (
            framebuffer_width,
            framebuffer_height,
        ):
            self._update_texture(score, framebuffer_width, framebuffer_height)

        glUseProgram(self.program)
        glBindVertexArray(self.vertex_array_object)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

    def shutdown(self):
        glDeleteTextures(1, [self.texture_id])
        glDeleteBuffers(1, [self.vertex_buffer])
        glDeleteBuffers(1, [self.element_buffer])
        glDeleteVertexArrays(1, [self.vertex_array_object])
        glDeleteProgram(self.program)
