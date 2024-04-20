from __future__ import annotations

from typing import Tuple

import pygame

from background import Background
from build_button import BuildButton, ArrowTowerBuildButton
from paths.chemin import Chemin
from mobs.goblinfactory import GoblinFactory
from interface.image_repository import ImageRepository
from buildings.tour import Tours
from player import Player
from wave import Wave, Waves
from wave_announcer import WaveAnnouncer

pygame.init()


class App:

    def __init__(self, width=800, height=600):
        self._running = False
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tower Defense LaMalice")
        self._image_repository = ImageRepository(width, height)
        self._current_wave_index = 0
        self.game_started = False
        self._announcer = WaveAnnouncer(screen=self.screen)
        self.show_build_menu = False
        self.show_preview_tower = False

        self._player = Player()
        self._background = Background(screen=self.screen,
                                      background_surface=self._image_repository.surface("background"))
        self.path = Chemin()
        self.arrow_towers = Tours(screen=self.screen, image=self._image_repository.surface("tower"),
                                  arrow_image=self._image_repository.surface("arrow"))
        self.goblins_factory = GoblinFactory(screen=self.screen, image=self._image_repository.surface("mob"))
        self._waves = Waves()
        self._waves.register_wave(wave=Wave(goblin_factory=self.goblins_factory, enemy_hp=4, num_enemies=10))
        self._waves.register_wave(wave=Wave(goblin_factory=self.goblins_factory, enemy_hp=5, num_enemies=7))

        self._build_button = BuildButton(
            screen=self.screen,
            label='Build',
            position=((width - 100) / 2, height - 50),
            dimensions=(100, 40),
            font=pygame.font.SysFont('Arial', 24)
        )
        self.arrow_tower_button = ArrowTowerBuildButton(
            screen=self.screen,
            position=((width - 200) / 2, height - 100),
            dimensions=(200, 40),
            font=pygame.font.SysFont('Arial', 24),
            on_click=self.activate_build_mode
        )

    def activate_build_mode(self):
        self.build_mode = True

    def run(self) -> None:
        self._running = True

        while self._running:
            self._background.draw()

            current_time = self._handle_event()

            if not self.game_started:
                self._draw_when_game_has_not_started()

            else:
                show_wave_announcement = self._waves.run(current_time=current_time)
                self._announcer.run(show_wave_announcement=show_wave_announcement,
                                    wave_current_index=self._waves.current_index,
                                    current_time=current_time)
                self._tick(current_time=current_time)
                self._draw_when_game_has_started()

            if self.show_build_menu:
                self.arrow_tower_button.draw()

            pygame.display.flip()

    def _draw_when_game_has_not_started(self):
        self._background.draw()
        self._build_button.draw()
        if self.show_preview_tower:
            self.draw_preview_tower(mouse_position=pygame.mouse.get_pos())

    def _draw_when_game_has_started(self):
        self._announcer.display_wave_info(wave_number=self._waves.current_index)
        self._build_button.draw()
        self._waves.draw_ennemies()
        self.arrow_towers.draw()
        if self.show_preview_tower:
            self.draw_preview_tower(mouse_position=pygame.mouse.get_pos())

    def draw_preview_tower(self, mouse_position: Tuple[int, int]):
        self.screen.blit(self._image_repository.surface("preview_tower"), mouse_position)

    def _handle_event(self):
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._build_button.is_clicked(event):
                    self.show_build_menu = not self.show_build_menu
                elif self.show_build_menu and self.arrow_tower_button.is_clicked(event):
                    self.arrow_tower_button.click()
                    self.show_preview_tower = True
                elif self.show_preview_tower:
                    if Player.can_buy(amount=20):
                        Player.spend_gold(amount=20)
                        self.build_tour_at(pygame.mouse.get_pos())
                    self.game_started = True
                    self.show_build_menu = False

        return current_time

    def build_tour_at(self, position: Tuple[int, int]) -> None:
        self.arrow_towers.add_tour(position=position, range=300, damage=1)
        self.show_preview_tower = False

    def _tick(self, current_time: int) -> None:
        self._waves.move_ennemies()
        self.arrow_towers.attack(current_time=current_time, ennemis=self._waves.ennemies())

        pygame.time.wait(10)
