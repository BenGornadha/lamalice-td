import pygame
import sys

from chemin import Chemin
from ennemi import Ennemi
from tour import Tour

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Définir le titre de la fenêtre
pygame.display.set_caption("Tower Defense LaMalice")
background_image = pygame.image.load('images/background.png')
background_image = pygame.transform.scale(background_image, (width, height))

tower_image = pygame.image.load('images/tour.png').convert_alpha()  # convert_alpha() est utilisé pour respecter la transparence
tower_image = pygame.transform.scale(tower_image, (40, 60))


chemin = Chemin()
tour = Tour(position=(50,205),portee=20,degats=1)
# enemy_position = chemin.get_path_points()[0]
# enemy_index = 0
mob = Ennemi(chemin=chemin.get_path_points(), vitesse=1, sante=100)
# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mob.deplacer()
    screen.blit(background_image, (0, 0))
    screen.blit(tower_image,tour.position)
    pygame.draw.circle(screen, (255, 0, 0), mob.position, 5)
    # Mettre à jour l'affichage
    pygame.display.flip()
    pygame.time.wait(100)
# Quitter proprement Pygame
pygame.quit()
sys.exit()
