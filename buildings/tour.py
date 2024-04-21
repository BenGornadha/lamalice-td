from __future__ import annotations
from typing import List

import pygame

from attacks.arrow import Arrow
from buildings.building import Building
from mobs.goblin import Goblin
from player import Player


class Tours:
    def __init__(self, screen, image, arrow_image) -> None:
        self._screen = screen
        self._image = image
        self._arrow_image = arrow_image
        self._tours = []

    @property
    def towers(self) -> List[Tour]:
        return self._tours

    def n_towers(self):
        return len(self._tours)

    def attack(self,current_time: int, ennemis: List[Goblin]):
        for tour in self._tours:
            tour.attack(current_time=current_time,ennemis=ennemis)

    def add_tour(self, position: tuple, range: int= 200, damage: float = 50):
        self._tours.append(
            Tour(screen=self._screen,
                 image=self._image,
                 arrow_image=self._arrow_image,
                 position=position,
                 range=range,
                 damage=damage))

    def draw(self):
        for tour in self._tours:
            tour.draw()

class Tour(Building):
    def __init__(self, screen, image, arrow_image, position: tuple, range: int, damage: float):
        self._screen = screen
        self._image = image
        self._position = position
        self._portee = range
        self._damage = damage
        self._level = 0
        self._last_attack_time = 0
        self._attack_cooldown = 500
        self.arrow = Arrow(screen=screen, image=arrow_image)
        self.font = pygame.font.Font(None, 24)  # Définir la police ici
        self.show_level_up = False  # Un indicateur pour afficher l'option de mise à niveau

    def is_clicked(self, mouse_pos):
        rect = pygame.Rect(self._position[0], self._position[1], self._image.get_width(), self._image.get_height())
        if rect.collidepoint(mouse_pos):
            self.show_level_up = not self.show_level_up  # Basculer l'affichage de l'option de mise à niveau
            return True
        return False

    def draw_level_up_option(self):
        if self.show_level_up:
            text = "Level up for 20 coins"
            # Assurez-vous que la police a été définie quelque part dans le constructeur de la classe
            label = self.font.render(text, True, (255, 255, 255))

            # Calcul de la position du texte et du rectangle d'affichage
            label_rect = label.get_rect(center=(self._position[0] + 50, self._position[1] - 20))
            self.level_up_rect = label_rect.inflate(20, 10)  # Ajout d'un peu plus d'espace autour du texte

            # Dessin du fond avec une bordure plus stylisée
            background_color = (50, 50, 50)  # Gris foncé pour le fond
            border_color = (200, 200, 200)  # Gris clair pour la bordure
            pygame.draw.rect(self._screen, border_color, self.level_up_rect)  # Bordure
            pygame.draw.rect(self._screen, background_color, self.level_up_rect.inflate(-4, -4))  # Fond

            # Dessiner une ombre pour le texte
            shadow_color = (50, 50, 50)
            shadow_offset = 2
            shadow_rect = label_rect.move(shadow_offset, shadow_offset)
            self._screen.blit(self.font.render(text, True, shadow_color), shadow_rect)

            # Dessin du texte
            self._screen.blit(label, label_rect)

    def attack(self, current_time: int, ennemis: List[Goblin]) -> None:
        self._current_arrow(current_time=current_time)
        if not self._can_attack(current_time=current_time):
            return
        target = self._trouver_ennemi_le_plus_proche_de_la_sortie(ennemis=ennemis)
        if target is None:
            return
        self._launch_new_arrow(current_time=current_time, to=target)

    def lvp_up(self, new_image):
        self._damage = self._damage * 2
        self._attack_cooldown = self._attack_cooldown * 0.8
        self._image = new_image

    def _current_arrow(self, current_time: int):
        if self.arrow.is_already_launch():
            self.arrow.animation(current_pygame_time=current_time, last_attack_time=self._last_attack_time)

            if self.arrow.has_reach_mob():
                self.arrow.target.subir_degats(self._damage)
                if self.arrow.target.is_dead():
                    Player.earn_gold(amount=1)
                self.arrow.reset_position()
                self.arrow.reset_target()

    def _trouver_ennemi_le_plus_proche_de_la_sortie(self, ennemis: List[Goblin]) -> Goblin | None:
        ennemis_a_portee = [ennemi for ennemi in ennemis if self._ennemi_a_portee(ennemi)]
        if ennemis_a_portee:
            return min(ennemis_a_portee, key=lambda ennemi: self._compute_distance_to_exit(ennemi.position))

    def _ennemi_a_portee(self, ennemi: Goblin) -> bool:
        distance = self._compute_distance_for(position=ennemi.position)
        if distance:
            return distance <= self._portee
        return False

    def _launch_new_arrow(self, current_time: int, to: Goblin):
        self.arrow.set_position(x=self.position[0], y=self.position[1])
        self._last_attack_time = current_time
        self.arrow.lock_target(mob=to)

    def draw(self):
        self._screen.blit(self._image, self._position)
        if self.arrow.position is not None:
            self.arrow.draw()
            self.draw_level_up_option()
