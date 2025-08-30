import pygame
import time
import os


class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.is_loaded = False
        self.file_path = None
        self.length = 0
        self._paused = False
        pygame.mixer.music.set_volume(0.8)

    def load(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        pygame.mixer.music.load(file_path)
        self.file_path = file_path
        # Estimating length via Sound for WAV, and fallback timer for MP3 (approx)
        try:
            snd = pygame.mixer.Sound(file_path)
            self.length = snd.get_length()
        except Exception:
            self.length = 0
        self.is_loaded = True
        self._paused = False

    def play(self):
        if not self.is_loaded:
            return
        if self._paused:
            pygame.mixer.music.unpause()
            self._paused = False
        else:
            pygame.mixer.music.play()

    def pause(self):
        if not self.is_loaded:
            return
        pygame.mixer.music.pause()
        self._paused = True

    def stop(self):
        if not self.is_loaded:
            return
        pygame.mixer.music.stop()
        self._paused = False

    def set_volume(self, volume: float):
        volume = max(0.0, min(1.0, float(volume)))
        pygame.mixer.music.set_volume(volume)

    def get_time(self):
        """
        Returns (elapsed_seconds, total_seconds approx)
        Note: pygame returns milliseconds since music started; resets on stop.
        """
        if not self.is_loaded:
            return 0.0, 0.0
        elapsed_ms = pygame.mixer.music.get_pos()
        elapsed_sec = max(0.0, elapsed_ms / 1000.0)
        total = self.length if self.length > 0 else 0.0
        return elapsed_sec, total
