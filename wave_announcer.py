import pygame
from pygame import Surface


class WaveAnnouncer:
    def __init__(self, screen : Surface):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 48)
        self.wave_announcement_time = 0
        self.wave_announcement_shown = False

    def display_wave_info(self, wave_number):
        wave_text = self.font.render(f'Wave: {wave_number + 1}', True, (255, 255, 255))
        self.screen.blit(wave_text, (self.screen.get_width() - wave_text.get_width() - 10, 10))

    def display_wave_announcement(self, wave_number):
        announcement_text = self.big_font.render(f'Wave {wave_number + 1}', True, (255, 0, 0))
        text_rect = announcement_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(announcement_text, text_rect)

    def update_announcement(self, current_wave_index, current_time):
        if not self.wave_announcement_shown:
            self.wave_announcement_time = current_time
            self.wave_announcement_shown = True

        show_wave_announcement = current_time - self.wave_announcement_time < 2000
        if show_wave_announcement:
            self.display_wave_announcement(current_wave_index)

        return show_wave_announcement

    def reset(self):
        self.wave_announcement_shown = False