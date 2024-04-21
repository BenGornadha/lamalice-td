import pygame
from pygame import Surface

from paths.chemin import Chemin


class Goblin:
    def __init__(self, screen: Surface, image: Surface, vitesse=1, sante=200):
        self._screen = screen
        self._image = image
        self._chemin = Chemin().get_path_points()
        self._vitesse = vitesse
        self._sante = sante
        self._max_sante = sante
        self._position_index = 0
        self._position = self._chemin[0]

    def is_alive(self) -> bool:
        return self._sante > 0

    def is_dead(self):
        return self._sante <= 0

    @property
    def position(self) -> tuple:
        return self._position

    def deplacer(self):
        self._position_index += self._vitesse
        if self._position_index >= len(self._chemin):
            self._position_index = 0  # Remet l'ennemi au début du chemin

        self._position = self._chemin[self._position_index]

    def subir_degats(self, degats):
        self._sante -= degats
        if self._sante <= 0:
            self.mourir()

    def mourir(self):
        self._position = None

    def draw(self):
        if self.is_alive():
            self._screen.blit(self._image, self.position)
            self.draw_health_bar()

    def draw_health_bar(self):
        # Dimensions et position de la barre de vie
        bar_width = 40
        bar_height = 5
        bar_x = self.position[0] + (self._image.get_width() - bar_width) / 2  # Centre la barre sur le gobelin
        bar_y = self.position[1] - bar_height - 2  # Un peu au-dessus du gobelin

        # Calcul du pourcentage de santé restante
        health_percentage = self._sante / self._max_sante

        # Couleur de la barre de santé qui change de vert à rouge
        health_color = (255 * (1 - health_percentage), 255 * health_percentage, 0)

        # Dessiner le fond de la barre de vie
        pygame.draw.rect(self._screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))
        # Dessiner la barre de vie actuelle
        pygame.draw.rect(self._screen, health_color, (bar_x, bar_y, bar_width * health_percentage, bar_height))

