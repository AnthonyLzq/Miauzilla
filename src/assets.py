import random

import pyrr
from PIL import Image

from .config import (
    OBSTACLE_SPAWN_X_RANGE,
    OBSTACLE_SPAWN_Y,
    OBSTACLE_SPAWN_Z_RANGE,
    TEXTURE_PATHS,
)


def load_texture_assets():
    texture_surfaces = []
    texture_data = []

    for texture_path in TEXTURE_PATHS:
        # PIL loads images top-down, but our OpenGL texture coordinates expect bottom-up.
        texture_surface = Image.open(texture_path).transpose(Image.FLIP_TOP_BOTTOM)
        texture_surfaces.append(texture_surface)
        texture_data.append(texture_surface.convert("RGBA").tobytes())

    return texture_surfaces, texture_data


def random_spawn_position():
    return pyrr.Vector3(
        [
            float(random.randint(*OBSTACLE_SPAWN_X_RANGE)),
            OBSTACLE_SPAWN_Y,
            float(random.randint(*OBSTACLE_SPAWN_Z_RANGE)),
        ]
    )
