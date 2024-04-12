from __future__ import annotations

import pygame

from chemin import Chemin
from ennemi import Ennemi
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
        self.path = Chemin()
        self.tower = Tour(position=(50, 205), portee=20, degats=1)
        self.mob = Ennemi(chemin=self.path.get_path_points(), vitesse=1, sante=100)

    def load_images(self):
        self._image_loader.register_background()
        self._image_loader.register_tower()

    def run(self) -> None:
        self._running = True
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            self.tick()

    def tick(self) -> None:
        self.mob.deplacer()

        self._draw()
        # Mettre à jour l'affichage
        pygame.display.flip()
        pygame.time.wait(100)

    def _draw(self):
        self.screen.blit(self._image_loader.image("background"), (0, 0))
        self.screen.blit(self._image_loader.image("tower"), self.tower.position)
        pygame.draw.circle(self.screen, (255, 0, 0), self.mob.position, 5)
