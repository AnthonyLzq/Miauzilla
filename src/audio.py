import sys

import pygame

from .config import BACKGROUND_MUSIC_PATH, HIT_SOUND_PATH


class AudioManager:
    def __init__(self):
        self.hit_sound = None
        self.background_music = None
        self.background_music_channel = None
        self.audio_enabled = False

    def initialize(self):
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

    def play_hit(self):
        if self.hit_sound is not None:
            self.hit_sound.play()

    def shutdown(self):
        if self.audio_enabled:
            pygame.mixer.music.stop()
            if self.background_music_channel is not None:
                self.background_music_channel.stop()
        pygame.quit()
