from __future__ import annotations

from typing import Tuple

import pygame
from pygame import Surface

from build_button import Button, ArrowTowerButton
from draw.draw import Drawer
from paths.chemin import Chemin
from mobs.goblins import Goblins
from interface.image_repository import ImageRepository
from buildings.tour import Tour
from wave import Wave
from wave_announcer import WaveAnnouncer

pygame.init()


class Background:

    def __init__(self, screen, background_surface: Surface) -> None:
        self._screen = screen
        self._background_surface = background_surface

    def draw(self):
        self._screen.blit(self._background_surface, (0, 0))


class App:

    def __init__(self, width=800, height=600):
        self._running = False
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tower Defense LaMalice")
        self._image_repository = ImageRepository(width, height)
        self._drawer = Drawer(screen=self.screen, image_repository=self._image_repository)
        self._background = Background(screen=self.screen,
                                      background_surface=self._image_repository.surface("background"))
        self.path = Chemin()
        self.arrow_towers = []
        self.goblins = Goblins(screen=self.screen,image=self._image_repository.surface("mob"))
        self._waves = [Wave(goblin_factory=self.goblins, enemy_hp=2, num_enemies=7),
                       Wave(goblin_factory=self.goblins, enemy_hp=3, num_enemies=6)]
        self._current_wave_index = 0
        self.game_started = False
        self._announcer = WaveAnnouncer(screen=self.screen)
        self._build_button = Button(
            screen=self.screen,
            label='Build',
            position=((width - 100) / 2, height - 50),
            dimensions=(100, 40),
            font=pygame.font.SysFont('Arial', 24)
        )
        self.arrow_tower_button = ArrowTowerButton(
            screen=self.screen,
            position=((width - 200) / 2, height - 100),
            dimensions=(200, 40),
            font=pygame.font.SysFont('Arial', 24),
            on_click=self.activate_build_mode
        )
        self.show_build_menu = False
        self.show_preview_tower = False

    def activate_build_mode(self):
        """ Active le mode de placement de la tour. """
        self.build_mode = True

    def run(self) -> None:
        self._running = True

        while self._running:
            current_time = self._handle_event()
            self._background.draw()
            self._build_button.draw()

            if not self.game_started:
                if self.show_preview_tower:
                    self._drawer.draw_preview_tower(mouse_position=pygame.mouse.get_pos())

            else:
                current_wave = self._waves[self._current_wave_index]
                self._handle_wave(current_time, current_wave)
                show_wave_announcement = self._announcer.update_announcement(self._current_wave_index, current_time)
                self._tick(current_time=current_time)
                if show_wave_announcement:
                    self._announcer.display_wave_announcement(self._current_wave_index)
                self._drawer.draw(goblins=self.goblins.goblins, towers=self.arrow_towers)
                self._announcer.display_wave_info(self._current_wave_index)

            if self.show_build_menu:
                self.arrow_tower_button.draw()

            pygame.display.flip()

    def _handle_event(self):
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._build_button.is_clicked(event):
                    self.show_build_menu = not self.show_build_menu  # Affiche ou masque le menu
                elif self.show_build_menu and self.arrow_tower_button.is_clicked(event):
                    self.arrow_tower_button.click()  # Utilise la méthode click du bouton
                    self.show_preview_tower = True
                elif not self.game_started and self.show_preview_tower:
                    self.build_tour_at(pygame.mouse.get_pos())
                    self.game_started = True
        return current_time

    def _handle_wave(self, current_time: int, current_wave: Wave) -> None:
        if not current_wave.all_enemies_spawned():
            current_wave.spawn_enemies(current_time)
        elif current_wave.all_enemies_defeated():
            self._next_wave()

    def _next_wave(self) -> None:
        if self._current_wave_index + 1 < len(self._waves):
            self._current_wave_index += 1
            self._announcer.reset()

    def build_tour_at(self, position: Tuple[int, int]) -> None:
        new_tower = Tour(position=position, range=300, damage=1)
        self.arrow_towers.append(new_tower)

    def _tick(self, current_time: int) -> None:
        self.goblins.move()
        for tower in self.arrow_towers:
            tower.attack(current_time=current_time, ennemis=self.goblins.goblins)

        pygame.display.flip()
        pygame.time.wait(1)
