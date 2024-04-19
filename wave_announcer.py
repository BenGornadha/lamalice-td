import pygame
from pygame import Surface


class WaveAnnouncer:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 48)
        self.wave_announcement_time = 0
        self.first_ever_wave_time = -1

    def _display_wave_info(self, wave_number):
        wave_text = self.font.render(f'Wave: {wave_number + 1}', True, (255, 255, 255))
        self.screen.blit(wave_text, (self.screen.get_width() - wave_text.get_width() - 10, 10))

    def display_wave_announcement(self, wave_number : int, current_time : int):
        announcement_text = self.big_font.render(f'Wave {wave_number + 1}', True, (255, 0, 0))
        text_rect = announcement_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(announcement_text, text_rect)


    def run(self, show_wave_announcement: bool, wave_current_index: int, current_time: int) -> None:
        self._display_wave_info(wave_number=wave_current_index)
        self._first_ever_wave_announcement(current_time=current_time, wave_current_index=wave_current_index)

        if show_wave_announcement :
            self.wave_announcement_time = current_time

        if self._show_wave_announcement_2_secs(current_time=current_time):
            self.display_wave_announcement(wave_number=wave_current_index,current_time=current_time)

    def _first_ever_wave_announcement(self, current_time, wave_current_index):
        if wave_current_index == 0 :
            if self.first_ever_wave_time == - 1:
                self.first_ever_wave_time = current_time
            if self._show_first_ever_wave_announcement_2_secs(current_time=current_time):
                self.display_wave_announcement(wave_number=wave_current_index,current_time=current_time)

    def _show_wave_announcement_2_secs(self, current_time: int) -> bool:
        return current_time - self.wave_announcement_time < 2000

    def _show_first_ever_wave_announcement_2_secs(self, current_time: int) -> bool:
        return current_time - self.first_ever_wave_time < 2000

