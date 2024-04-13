from typing import List

import pygame
from pygame import Rect

from chemin import Chemin
from goblin import Goblin


def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


class Tour:
    def __init__(self, position: tuple, portee: int, degats: int, weapon: Rect):
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
        self.current_ennemi = Goblin(chemin=Chemin().get_path_points(), vitesse=0, sante=0)

    @property
    def position(self):
        return self._position

    def _compute_distance_for(self, position: tuple) -> int:
        if position:
            return ((self._position[0] - position[0]) ** 2 + (self._position[1] - position[1]) ** 2) ** 0.5

    def _ennemi_a_portee(self, ennemi: Goblin) -> bool:
        distance = self._compute_distance_for(position=ennemi.position)
        if distance:
            return distance <= self._portee
        return False

    def trouver_ennemi_le_plus_proche_de_la_sortie(self, ennemis: List[Goblin], sortie=(800, 235)) -> Goblin | None:
        ennemis_a_portee = [ennemi for ennemi in ennemis if self._ennemi_a_portee(ennemi)]
        if ennemis_a_portee:
            return min(ennemis_a_portee, key=lambda ennemi: distance(ennemi.position, sortie))

    def attaquer2(self, current_time: int, ennemis: List[Goblin]):
        self._current_arrow(current_time)
        target = self.trouver_ennemi_le_plus_proche_de_la_sortie(ennemis=ennemis)
        if target and target.is_alive() and not self._ennemi_a_portee(ennemi=target):
            return
        if target and self._reload(current_time=current_time):
            self._launch_new_arrow(current_time=current_time, to=target)

    def attaquer(self, current_time: int, ennemi: Goblin):
        self._current_arrow(current_time, ennemi)

        if ennemi.is_alive() and not self._ennemi_a_portee(ennemi=ennemi):
            return
        if self._reload(current_time=current_time):
            self._launch_new_arrow(current_time=current_time, to=ennemi)

    def _current_arrow(self, current_time: int):
        if self._arrow_already_launched():
            self._animation_arrow(current_time=current_time)

            if self._arrow_reach_mob(ennemi=self.current_ennemi):
                self.arrow_pos = None
                self.current_ennemi.subir_degats(self._degats)
                self.current_ennemi = None

    def _arrow_reach_mob(self, ennemi: Goblin):
        return pygame.math.Vector2(self.arrow_pos).distance_to(ennemi.position) < 10

    def _animation_arrow(self, current_time: int):
        if self.current_ennemi is None:
            return
        if self.current_ennemi.position:
            direction = pygame.math.Vector2(self.current_ennemi.position) - pygame.math.Vector2(self.arrow_pos)
            if direction.length() > 0:
                direction = direction.normalize()
            self.arrow_pos[0] += direction.x * self.arrow_speed * (current_time - self.last_attack_time) / 1000.0
            self.arrow_pos[1] += direction.y * self.arrow_speed * (current_time - self.last_attack_time) / 1000.0

    def _arrow_already_launched(self):
        return self.arrow_pos is not None

    def _reload(self, current_time: int) -> bool:
        return current_time - self.last_attack_time > self.attack_cooldown

    def _launch_new_arrow(self, current_time: int, to: Goblin):
        self.arrow_pos = list(self.position)
        self.last_attack_time = current_time
        self.current_ennemi = to
