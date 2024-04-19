from typing import List

from pygame import Surface

from mobs.goblin import Goblin


class GoblinFactory:
    def __init__(self, screen: Surface, image: Surface) -> None:
        self._screen = screen
        self._image = image

    def create_goblin(self, vitesse=1, sante=3) -> Goblin:
        return Goblin(screen=self._screen, image=self._image, vitesse=vitesse, sante=sante)


class Goblins:

    def __init__(self):
        self._goblins = []

    @property
    def goblins(self) -> List[Goblin]:
        return self._goblins

    def add_goblin(self, goblin: Goblin):
        self._goblins.append(goblin)

