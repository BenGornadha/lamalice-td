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
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)  # Choix de la police et de la taille
        self.big_font = pygame.font.SysFont('Arial', 48)  # Pour l'affichage central

        self._image_loader = ImageRepository(for_window=self._window)
        self.path = Chemin()
        self.arrow_tower = Tour(position=(50, 205), range=300, damage=1)
        self.goblins = Goblins()
        self._waves = [Wave(goblin_factory=self.goblins,enemy_hp=2,num_enemies=10),
                       Wave(goblin_factory=self.goblins,enemy_hp=3,num_enemies=15)]
        self._current_wave_index = 0

    def display_wave_info(self, wave_number):
        # Affiche le numéro de la vague en cours en haut à droite
        wave_text = self.font.render(f'Wave: {wave_number + 1}', True, (255, 255, 255))
        self.screen.blit(wave_text, (self.screen.get_width() - wave_text.get_width() - 10, 10))

    def display_wave_announcement(self, wave_number):
        # Affiche un gros message au centre de l'écran pour annoncer la nouvelle vague
        announcement_text = self.big_font.render(f'Wave {wave_number + 1}', True, (255, 0, 0))
        text_rect = announcement_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(announcement_text, text_rect)

    def _load_images(self) -> None:
        self._image_loader.register_surfaces()

    def run(self) -> None:
        self._running = True
        wave_announcement_shown = False  # Pour contrôler l'affichage de l'annonce
        wave_announcement_time = 0
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
                    wave_announcement_shown = False
            if not wave_announcement_shown:
                wave_announcement_time = current_time
                wave_announcement_shown = True
            self.tick(current_time, current_time - wave_announcement_time < 2000)

    def tick(self, current_time: int, show_wave_announcement) -> None:
        self.goblins.move()
        self.arrow_tower.attack(current_time=current_time, ennemis=self.goblins.goblins)

        self._draw(show_wave_announcement=show_wave_announcement)
        pygame.display.flip()
        pygame.time.wait(10)

    def _draw(self,show_wave_announcement : bool) -> None:
        self.screen.blit(self._image_loader.surface("background"), (0, 0))
        self.screen.blit(self._image_loader.surface("tower"), self.arrow_tower.position)
        self.display_wave_info(self._current_wave_index)
        for goblin in self.goblins.goblins:
            if goblin.is_alive():
                self.screen.blit(self._image_loader.surface("mob"), goblin.position)
        if self.arrow_tower.arrow.position is not None:
            self.screen.blit(self._image_loader.surface("arrow"), self.arrow_tower.arrow.position)
        if show_wave_announcement:
            self.display_wave_announcement(self._current_wave_index)
