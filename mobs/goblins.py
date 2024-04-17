from typing import List

from pygame import Surface

from mobs.goblin import Goblin


class Goblins:
    def __init__(self, screen: Surface, image: Surface) -> None:
        self._screen = screen
        self._image = image
        self._goblins = []
        self.create_goblin()

    @property
    def goblins(self) -> List[Goblin]:
        return self._goblins

    def create_goblin(self, vitesse=1, sante=3) -> None:
        self._goblins.append(Goblin(screen=self._screen, image=self._image, vitesse=vitesse, sante=sante))

    def move(self) -> None:
        for goblin in self._goblins:
            if goblin.is_alive():
                goblin.deplacer()

    def draw(self):
        for goblin in self.goblins:
            goblin.draw()
