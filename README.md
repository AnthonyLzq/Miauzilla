# Miauzilla

Miauzilla is a small 3D endless runner built with Python, GLFW, PyOpenGL, and pygame. You control a giant cat made of cubes and crash into buildings to score points.

## Current status

The project was revived to run on a modern Python codebase again:

- explicit dependency installation through `requirements.txt`
- asset loading relative to the project instead of the current shell directory
- runtime initialization moved out of import-time side effects
- compatibility fixes for current Python and desktop OpenGL
- runtime split into focused modules under `src/`
- on-screen score HUD rendered inside the game window

## Requirements

- Python 3.10+
- OpenGL-capable desktop environment
- audio output is optional; the game will still run if pygame cannot initialize the mixer

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

From the repository root:

```bash
python miauzilla.py
```

## Controls

- `W`, `A`, `S`, `D` or arrow keys: move Miauzilla
- `Q`: cycle camera
- `E`: cycle light direction
- `Esc`: quit

## Project layout

- `miauzilla.py`: thin top-level entrypoint that preserves the original run command
- `src/index.py`: package entrypoint
- `src/game.py`: main loop and gameplay orchestration
- `src/rendering.py`: shaders, OpenGL objects, and buffer wiring
- `src/audio.py`: music and sound effect setup
- `src/assets.py`: texture loading and obstacle spawn helpers
- `src/config.py`: paths, window settings, and game constants
- `src/geometry.py`: cube and quad geometry data
- `src/hud.py`: score overlay rendered on top of the 3D scene
- `src/window.py`: GLFW window and input callbacks
- `textures/`: textures used by obstacles, the cat, the ground, and the sky
- `music/`: background music and hit sound
- `changelog.md`: historical milestones for the project

## Authors

- **Anthony Luzquiños** - Initial work and documentation - [AnthonyLzq](https://github.com/AnthonyLzq)
- Contributors from the original course project can be found in the repository history
