from __future__ import annotations

import pygame

from chemin import Chemin
from goblins import Goblins
from image_repository import ImageRepository
from tour import Tour
from window import Window

pygame.init()


class App:

    def __init__(self, width=800, height=600):
        self._running = False
        self._window = Window(width=width, height=height)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tower Defense LaMalice")
        self._image_loader = ImageRepository(for_window=self._window)
        self._load_images()
        self.path = Chemin()
        self.arrow_tower = Tour(position=(50, 205), portee=300, degats=1, weapon=self._image_loader.image("arrow"))
        self.goblins = Goblins()
        # self.goblin = Goblin(chemin=self.path.get_path_points(), vitesse=1, sante=3)

    def _load_images(self) -> None:
        self._image_loader.register_surfaces()

    def run(self) -> None:
        self._running = True
        while self._running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            self.tick(current_time)

    def tick(self, current_time: int) -> None:
        self.goblins.move()
        self.arrow_tower.attack(current_time=current_time, ennemis=self.goblins.goblins)
        # if self.goblin.is_alive():
        #     self.goblin.deplacer()
        #     self.arrow_tower.attaquer(current_time=current_time, ennemi=self.goblin)

        self._draw()
        # Mettre à jour l'affichage
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
