from __future__ import annotations

from pygame import Surface


class Background:

    def __init__(self, screen, background_surface: Surface) -> None:
        self._screen = screen
        self._background_surface = background_surface

    def draw(self):
        self._screen.blit(self._background_surface, (0, 0))
