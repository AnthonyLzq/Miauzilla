import ctypes

import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_ELEMENT_ARRAY_BUFFER,
    GL_FALSE,
    GL_FLOAT,
    GL_FRAGMENT_SHADER,
    GL_LINEAR,
    GL_REPEAT,
    GL_RGBA,
    GL_STATIC_DRAW,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_UNSIGNED_BYTE,
    GL_UNSIGNED_INT,
    GL_VERTEX_SHADER,
    glBindBuffer,
    glBindTexture,
    glBindVertexArray,
    glBufferData,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenTextures,
    glGenVertexArrays,
    glGenerateMipmap,
    glTexImage2D,
    glTexParameteri,
    glVertexAttribPointer,
)
from OpenGL.GL.shaders import compileProgram, compileShader

from .geometry import CUBE_INDICES, CUBE_VERTICES, QUAD_INDICES, QUAD_VERTICES


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


def _load_gl_texture(texture_surface, texture_bytes):
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
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
    return texture_id


class Cube:
    def __init__(self):
        self.vertices = np.array(CUBE_VERTICES, dtype=np.float32)
        self.indices = np.array(CUBE_INDICES, dtype=np.uint32)
        self.texture_id = 0

    def load_texture(self, texture_surface, texture_bytes):
        self.texture_id = _load_gl_texture(texture_surface, texture_bytes)


class Ground:
    def __init__(self):
        self.vertices = np.array(QUAD_VERTICES, dtype=np.float32)
        self.indices = np.array(QUAD_INDICES, dtype=np.uint32)
        self.texture_id = 0

    def load_texture(self, texture_surface, texture_bytes):
        self.texture_id = _load_gl_texture(texture_surface, texture_bytes)


class Shader:
    def __init__(self):
        self.program = compileProgram(
            compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER),
        )

    def bind_cubes(self, cubes):
        self.cube_vertex_array_objects = [0] * len(cubes)
        self.cube_vertex_buffers = [0] * len(cubes)
        self.cube_element_buffers = [0] * len(cubes)

        for index, cube in enumerate(cubes):
            self.cube_vertex_array_objects[index] = glGenVertexArrays(1)
            glBindVertexArray(self.cube_vertex_array_objects[index])

            self.cube_vertex_buffers[index] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.cube_vertex_buffers[index])
            glBufferData(GL_ARRAY_BUFFER, cube.vertices.nbytes, cube.vertices, GL_STATIC_DRAW)

            self.cube_element_buffers[index] = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.cube_element_buffers[index])
            glBufferData(
                GL_ELEMENT_ARRAY_BUFFER,
                cube.indices.nbytes,
                cube.indices,
                GL_STATIC_DRAW,
            )

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(
                0, 3, GL_FLOAT, GL_FALSE, cube.vertices.itemsize * 8, ctypes.c_void_p(0)
            )

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(
                1, 2, GL_FLOAT, GL_FALSE, cube.vertices.itemsize * 8, ctypes.c_void_p(12)
            )

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(
                2, 3, GL_FLOAT, GL_FALSE, cube.vertices.itemsize * 8, ctypes.c_void_p(20)
            )

    def bind_quads(self, quads):
        self.quad_vertex_array_objects = [0] * len(quads)
        self.quad_vertex_buffers = [0] * len(quads)
        self.quad_element_buffers = [0] * len(quads)

        for index, quad in enumerate(quads):
            self.quad_vertex_array_objects[index] = glGenVertexArrays(1)
            glBindVertexArray(self.quad_vertex_array_objects[index])

            self.quad_vertex_buffers[index] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.quad_vertex_buffers[index])
            glBufferData(GL_ARRAY_BUFFER, quad.vertices.nbytes, quad.vertices, GL_STATIC_DRAW)

            self.quad_element_buffers[index] = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.quad_element_buffers[index])
            glBufferData(
                GL_ELEMENT_ARRAY_BUFFER,
                quad.indices.nbytes,
                quad.indices,
                GL_STATIC_DRAW,
            )

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(
                0, 3, GL_FLOAT, GL_FALSE, quad.vertices.itemsize * 8, ctypes.c_void_p(0)
            )

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(
                1, 2, GL_FLOAT, GL_FALSE, quad.vertices.itemsize * 8, ctypes.c_void_p(12)
            )

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(
                2, 3, GL_FLOAT, GL_FALSE, quad.vertices.itemsize * 8, ctypes.c_void_p(20)
            )
