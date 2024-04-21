import pygame
from pygame import Surface

pygame.font.init()
class Player:
    gold = 50
    font = pygame.font.SysFont('Arial', 24)
    screen = None
    hearts = 20

    @classmethod
    def set_screen(cls, screen: Surface):
        cls.screen = screen

    @classmethod
    def earn_gold(cls, amount=1):
        cls.gold += amount

    @classmethod
    def can_buy(cls, amount: int):
        return cls.gold >= amount

    @classmethod
    def spend_gold(cls, amount: int):
        cls.gold -= amount

    @classmethod
    def display_current_money(cls):
        wave_text = cls.font.render(f'Coins: {cls.gold}', True, (255, 255, 255))
        cls.screen.blit(wave_text, (cls.screen.get_width() - wave_text.get_width() - 10, 30))

    @classmethod
    def display_current_lives(cls):
        wave_text = cls.font.render(f'Hearts: {cls.hearts}', True, (255, 255, 255))
        cls.screen.blit(wave_text, (cls.screen.get_width() - wave_text.get_width() - 10, 50))