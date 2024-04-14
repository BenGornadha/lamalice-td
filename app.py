from __future__ import annotations

import pygame

from paths.chemin import Chemin
from mobs.goblins import Goblins
from interface.image_repository import ImageRepository
from buildings.tour import Tour
from interface.window import Window
from wave import Wave

pygame.init()


class App:

    def __init__(self, width=800, height=600):
        self._running = False
        self._window = Window(width=width, height=height)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tower Defense LaMalice")

        self._image_loader = ImageRepository(for_window=self._window)
        self.path = Chemin()
        self.arrow_tower = Tour(position=(50, 205), range=300, damage=1)
        self.goblins = Goblins()
        self._waves = [Wave(goblin_factory=self.goblins,enemy_hp=2,num_enemies=15)]
        self._current_wave_index = 0

    def _load_images(self) -> None:
        self._image_loader.register_surfaces()

    def run(self) -> None:
        self._running = True
        while self._running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            current_wave = self._waves[self._current_wave_index]
            if not current_wave.all_enemies_spawned():
                current_wave.spawn_enemies(current_time)
            elif current_wave.all_enemies_defeated():
                if self._current_wave_index + 1 < len(self._waves):
                    self._current_wave_index += 1
            # if current_time - last_mob_pop > 1000:
            #     self.goblins.create_goblin()
            #     last_mob_pop = current_time
            self.tick(current_time)

    def tick(self, current_time: int) -> None:
        self.goblins.move()
        self.arrow_tower.attack(current_time=current_time, ennemis=self.goblins.goblins)

        self._draw()
        pygame.display.flip()
        pygame.time.wait(10)

    def _draw(self) -> None:
        self.screen.blit(self._image_loader.surface("background"), (0, 0))
        self.screen.blit(self._image_loader.surface("tower"), self.arrow_tower.position)
        for goblin in self.goblins.goblins:
            if goblin.is_alive():
                self.screen.blit(self._image_loader.surface("mob"), goblin.position)
        if self.arrow_tower.arrow.position is not None:
            self.screen.blit(self._image_loader.surface("arrow"), self.arrow_tower.arrow.position)
