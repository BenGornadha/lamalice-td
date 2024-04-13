import pygame
from pygame import Rect

from ennemi import Ennemi


class Tour:
    def __init__(self, position: tuple, portee: int, degats: int, weapon: Rect):
        """
        Initialise une nouvelle tour.

        :param position: Un tuple (x, y) représentant la position de la tour sur le plateau.
        :param portee: Un entier indiquant la portée d'attaque de la tour (distance à laquelle elle peut attaquer les ennemis).
        :param degats: Les dégâts infligés par la tour à chaque attaque.
        """
        self._position = position
        self._portee = portee
        self._degats = degats
        self._weapon = weapon
        self._last_attack_time = 0
        self.arrow_pos = None
        self.target_pos = None
        self.arrow_speed = 500  # Pixels par seconde
        self.last_attack_time = 0
        self.attack_cooldown = 1000

    @property
    def position(self):
        return self._position

    def _ennemi_a_portee(self, ennemi: Ennemi):
        ennemi_position = ennemi._position
        distance = ((self._position[0] - ennemi_position[0]) ** 2 + (
                self._position[1] - ennemi_position[1]) ** 2) ** 0.5
        return distance <= self._portee

    def attaquer(self, current_time, ennemi: Ennemi):
        self._current_arrow(current_time, ennemi)

        if not self._ennemi_a_portee(ennemi=ennemi):
            return
        if self._reload(current_time=current_time):
            self._launch_new_arrow(current_time=current_time)

    def _current_arrow(self, current_time, ennemi):
        if self._arrow_alread_launched(ennemi=ennemi):
            self._animation_arrow(current_time=current_time, ennemi=ennemi)

            if self._arrow_reach_mob(ennemi=ennemi):
                self.arrow_pos = None  # Réinitialise l'animation
                ennemi.subir_degats(self._degats)
            self.last_attack_time = current_time

    def _arrow_reach_mob(self, ennemi):
        return pygame.math.Vector2(self.arrow_pos).distance_to(ennemi.position) < 10

    def _animation_arrow(self, current_time, ennemi):
        direction = pygame.math.Vector2(ennemi.position) - pygame.math.Vector2(self.arrow_pos)
        if direction.length() > 0:  # Évite la division par zéro
            direction = direction.normalize()
        self.arrow_pos[0] += direction.x * self.arrow_speed * (current_time - self.last_attack_time) / 1000.0
        self.arrow_pos[1] += direction.y * self.arrow_speed * (current_time - self.last_attack_time) / 1000.0

    def _arrow_alread_launched(self, ennemi):
        return self.arrow_pos is not None and ennemi.position is not None

    def _reload(self, current_time: int) -> bool:
        return current_time - self.last_attack_time > self.attack_cooldown

    def _launch_new_arrow(self, current_time):
        # Commence une nouvelle animation de tir
        self.arrow_pos = list(self.position)  # Convertis le tuple en liste pour la mutabilité
        self.last_attack_time = current_time
