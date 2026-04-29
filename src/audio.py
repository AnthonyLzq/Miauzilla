import sys

import pygame

from .config import BACKGROUND_MUSIC_PATH, HIT_SOUND_PATH, INITIAL_MUSIC_VOLUME, VOLUME_STEP


class AudioManager:
    def __init__(self):
        self.hit_sound = None
        self.background_music = None
        self.background_music_channel = None
        self.audio_enabled = False
        self.music_uses_channel = False
        self.music_volume = INITIAL_MUSIC_VOLUME

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
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.audio_enabled = True
            self.music_uses_channel = False
        except pygame.error as music_error:
            try:
                self.background_music = pygame.mixer.Sound(BACKGROUND_MUSIC_PATH.as_posix())
                self.background_music.set_volume(self.music_volume)
                self.background_music_channel = self.background_music.play(loops=-1)
                self.audio_enabled = True
                self.music_uses_channel = True
            except pygame.error as fallback_error:
                print(
                    "Background music disabled: "
                    f"{music_error}. Fallback also failed: {fallback_error}",
                    file=sys.stderr,
                )

        try:
            self.hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH.as_posix())
            self.hit_sound.set_volume(self.music_volume)
            self.audio_enabled = True
        except pygame.error as error:
            print(f"Hit sound disabled: {error}", file=sys.stderr)

    def play_hit(self):
        if self.hit_sound is not None:
            self.hit_sound.play()

    def pause(self):
        if not self.audio_enabled:
            return

        if self.music_uses_channel and self.background_music_channel is not None:
            self.background_music_channel.pause()
        else:
            pygame.mixer.music.pause()

    def resume(self):
        if not self.audio_enabled:
            return

        if self.music_uses_channel and self.background_music_channel is not None:
            self.background_music_channel.unpause()
        else:
            pygame.mixer.music.unpause()

    def set_volume(self, volume):
        self.music_volume = min(max(volume, 0.0), 1.0)

        if not self.audio_enabled:
            return

        if self.music_uses_channel and self.background_music is not None:
            self.background_music.set_volume(self.music_volume)
        else:
            pygame.mixer.music.set_volume(self.music_volume)

        if self.hit_sound is not None:
            self.hit_sound.set_volume(self.music_volume)

    def adjust_volume(self, direction):
        self.set_volume(self.music_volume + (VOLUME_STEP * direction))
        return self.music_volume

    def get_volume_percentage(self):
        return int(round(self.music_volume * 100))

    def shutdown(self):
        if self.audio_enabled:
            pygame.mixer.music.stop()
            if self.background_music_channel is not None:
                self.background_music_channel.stop()
        pygame.quit()
