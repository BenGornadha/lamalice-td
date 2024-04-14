from __future__ import annotations

import pygame
from pygame import Surface, Rect

from window import Window


class ImageRepository:

    def __init__(self, for_window: Window) -> None:
        self._window = for_window
        self._surfaces = {}
        self._rects = {}
        self.register_surfaces()

    def register_surfaces(self):
        self._register_mob()
        self._register_background()
        self._register_tower()
        self._register_arrow()

    def surface(self, name: str) -> Surface:
        return self._surfaces[name]

    def image(self, name: str) -> Rect:
        return self._rects[name]

    def _register_background(self) -> None:
        background_image = pygame.image.load("./images/background.png")
        self._surfaces["background"] = pygame.transform.scale(background_image,
                                                              (self._window.width, self._window.height))

    def _register_tower(self) -> None:
        tower_image = pygame.image.load(
            'images/tour.png').convert_alpha()  # convert_alpha() est utilisé pour respecter la transparence
        self._surfaces["tower"] = pygame.transform.scale(tower_image, (40, 60))

    def _register_arrow(self):
        arrow_surface = pygame.image.load('./images/arrow.png').convert_alpha()
        self._surfaces["arrow"] = pygame.transform.scale(arrow_surface, (10, 25))
        self._register_arrow_image(arrow_image=self._surfaces["arrow"])

    def _register_arrow_image(self, arrow_image: Surface):
        self._rects["arrow"] = arrow_image.get_rect()

    def _register_mob(self):
        mob_image = pygame.image.load("./images/goblin.png")
        self._surfaces["mob"] = pygame.transform.scale(mob_image, (20, 25))