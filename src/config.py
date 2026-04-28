from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Miauzilla"
HUD_FONT_SIZE = 36
HUD_MARGIN = 16
HUD_TEXT_COLOR = (255, 255, 255, 255)

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
OBSTACLE_SPAWN_X_RANGE = (-5, 4)
OBSTACLE_SPAWN_Y = 1.5
OBSTACLE_SPAWN_Z_RANGE = (-100, -41)

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
