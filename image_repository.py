from __future__ import annotations

import pygame
from pygame import Surface

from window import Window


class ImageRepository:

    def __init__(self, for_window: Window) -> None:
        self._window = for_window
        self._images = {}

    def register_background(self) -> None:
        background_image = pygame.image.load("./images/background.png")
        self._images["background"] = pygame.transform.scale(background_image, (self._window.width, self._window.height))

    def register_tower(self) -> None:
        tower_image = pygame.image.load(
            'images/tour.png').convert_alpha()  # convert_alpha() est utilisé pour respecter la transparence
        self._images["tower"] = pygame.transform.scale(tower_image, (40, 60))

    def image(self, name: str) -> Surface:
        return self._images[name]
