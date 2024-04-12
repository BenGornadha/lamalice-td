from __future__ import annotations
import pygame
from pygame import Surface

from chemin import Chemin
from ennemi import Ennemi
from tour import Tour

pygame.init()


class ImageRepository:

    def __init__(self, for_window: Window):
        self._window = for_window
        self._images = {}

    def register_background(self):
        background_image = pygame.image.load("./images/background.png")
        self._images["background"] = pygame.transform.scale(background_image, (self._window.width, self._window.height))

    def register_tour(self):
        tower_image = pygame.image.load(
            'images/tour.png').convert_alpha()  # convert_alpha() est utilisé pour respecter la transparence
        self._images["tower"] = pygame.transform.scale(tower_image, (40, 60))

    def image(self, name: str) -> Surface:
        return self._images[name]


class Window:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height


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
        self._image_loader.register_tour()

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
