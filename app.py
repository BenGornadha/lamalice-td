from __future__ import annotations

import pygame

from paths.chemin import Chemin
from mobs.goblins import Goblins
from interface.image_repository import ImageRepository
from buildings.tour import Tour
from wave import Wave
from wave_announcer import WaveAnnouncer

pygame.init()


class App:

    def __init__(self, width=800, height=600):
        self._running = False
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tower Defense LaMalice")
        pygame.font.init()

        self._image_loader = ImageRepository(width, height)
        self.path = Chemin()
        self.arrow_tower = Tour(position=(50, 205), range=300, damage=1)
        self.goblins = Goblins()
        self._waves = [Wave(goblin_factory=self.goblins, enemy_hp=2, num_enemies=7),
                       Wave(goblin_factory=self.goblins, enemy_hp=3, num_enemies=6)]
        self._current_wave_index = 0
        self.announcer = WaveAnnouncer(self.screen)

    def run(self) -> None:
        self._running = True
        while self._running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            current_wave = self._waves[self._current_wave_index]

            self._handle_wave(current_time, current_wave)

            show_wave_announcement = self.announcer.update_announcement(self._current_wave_index, current_time)

            self._tick(current_time=current_time)
            self._draw(show_wave_announcement=show_wave_announcement)

    def _handle_wave(self, current_time: int, current_wave: Wave) -> None:
        if not current_wave.all_enemies_spawned():
            current_wave.spawn_enemies(current_time)
        elif current_wave.all_enemies_defeated():
            self._next_wave()

    def _next_wave(self) -> None:
        if self._current_wave_index + 1 < len(self._waves):
            self._current_wave_index += 1
            self.announcer.reset()

    def _tick(self, current_time: int) -> None:
        self.goblins.move()
        self.arrow_tower.attack(current_time=current_time, ennemis=self.goblins.goblins)

        pygame.display.flip()
        pygame.time.wait(10)

    def _draw(self, show_wave_announcement: bool) -> None:
        self.screen.blit(self._image_loader.surface("background"), (0, 0))
        self.screen.blit(self._image_loader.surface("tower"), self.arrow_tower.position)
        for goblin in self.goblins.goblins:
            if goblin.is_alive():
                self.screen.blit(self._image_loader.surface("mob"), goblin.position)
        if self.arrow_tower.arrow.position is not None:
            self.screen.blit(self._image_loader.surface("arrow"), self.arrow_tower.arrow.position)
        self.announcer.display_wave_info(self._current_wave_index)
        if show_wave_announcement:
            self.announcer.display_wave_announcement(self._current_wave_index)
