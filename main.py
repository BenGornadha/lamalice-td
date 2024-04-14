import sys

import pygame

from app import App

if __name__ == '__main__':
    app = App()

    app.run()
    pygame.quit()
    sys.exit()