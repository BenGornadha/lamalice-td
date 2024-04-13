import sys

import pygame

from app import App

if __name__ == '__main__':
    app = App()
    app._load_images()

    app.run()
    pygame.quit()
    sys.exit()