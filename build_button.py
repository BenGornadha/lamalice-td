import pygame

class Button:
    def __init__(self, screen, label, position, dimensions, font, color=(0, 200, 0), text_color=(255, 255, 255)):
        self.screen = screen
        self.label = label
        self.position = position
        self.dimensions = dimensions
        self.font = font
        self.color = color
        self.text_color = text_color
        self.rect = pygame.Rect(position[0], position[1], dimensions[0], dimensions[1])

    def draw(self):
        # Dessine le rectangle du bouton
        pygame.draw.rect(self.screen, self.color, self.rect)
        # Dessine le texte au centre du bouton
        text_surface = self.font.render(self.label, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2))
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
