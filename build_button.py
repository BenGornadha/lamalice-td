import pygame

class BuildButton:
    def __init__(self, screen, label, position, dimensions, font, color=(0, 200, 0), text_color=(255, 255, 255)):
        self.screen = screen
        self.label = label
        self.position = position
        self.dimensions = dimensions
        self.font = font
        self.color = color
        self.text_color = text_color
        self.rect = pygame.Rect(position[0], position[1], dimensions[0], dimensions[1])

    def update_label(self, new_cost : int):
        self.label = f"Arrow Tower ({new_cost} coins)"


    def draw(self):
        shadow_color = (0, 0, 0, 50)  # Noir avec une transparence
        shadow_offset = 3  # Décalage de l'ombre en pixels

        shadow_rect = pygame.Rect(self.rect.x + shadow_offset, self.rect.y + shadow_offset, self.rect.width,
                                  self.rect.height)
        pygame.draw.rect(self.screen, shadow_color, shadow_rect)

        self.draw_gradient_rect(self.rect, (30, 144, 255), (173, 216, 230))  # Bleu dégradé

        text_surface = self.font.render(self.label, True, self.text_color)
        text_rect = text_surface.get_rect(
            center=(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2))
        self.screen.blit(text_surface, text_rect)

    def draw_gradient_rect(self, rect, color_start, color_end):
        height = rect.height
        for i in range(height):
            r, g, b = [x + (y - x) * i / height for x, y in zip(color_start, color_end)]
            pygame.draw.line(self.screen, (int(r), int(g), int(b)), (rect.x, rect.y + i),
                             (rect.x + rect.width, rect.y + i))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class ArrowTowerBuildButton(BuildButton):
    def __init__(self, screen, position, dimensions, font, cost, on_click):
        super().__init__(screen, label=f"Arrow Tower ({cost} coins)", position=position, dimensions=dimensions, font=font)
        self.on_click = on_click  # Callback pour gérer le clic sur le bouton

    def click(self, *args, **kwargs):
        self.on_click(*args, **kwargs)
