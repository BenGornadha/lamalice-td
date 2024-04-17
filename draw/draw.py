from __future__ import annotations

from typing import Tuple, List

import pygame
from pygame import Surface

from buildings.tour import Tour
from interface.image_repository import ImageRepository
from mobs.goblin import Goblin
from wave_announcer import WaveAnnouncer


class Drawer:

    def __init__(self, screen: Surface, image_repository: ImageRepository) -> None:
        self._screen = screen
        self._image_repository = image_repository
        self._announcer = WaveAnnouncer(self._screen)
        pygame.font.init()  # Assurez-vous que l'initialisation des polices est faite
        self.font = pygame.font.SysFont('Arial', 24)

    def draw(self, goblins, towers):
        # self.draw_background()
        self._draw_goblins(goblins=goblins)
        self._draw_towers(towers=towers)

    def draw_background(self) -> None:
        self._screen.blit(self._image_repository.surface("background"), (0, 0))

    def draw_preview_tower(self, mouse_position: Tuple[int, int]):
        self._screen.blit(self._image_repository.surface("preview_tower"), mouse_position)

    def _draw_towers(self, towers: List[Tour]) -> None:
        for tower in towers:
            self._screen.blit(self._image_repository.surface("tower"), tower.position)
            if tower.arrow.position is not None:
                self._screen.blit(self._image_repository.surface("arrow"), tower.arrow.position)

    def _draw_goblins(self, goblins: List[Goblin]) -> None:
        for goblin in goblins:
            if goblin.is_alive():
                self._screen.blit(self._image_repository.surface("mob"), goblin.position)
