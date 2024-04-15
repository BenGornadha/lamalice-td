from typing import List

from mobs.goblin import Goblin
from paths.chemin import Chemin


class Goblins:
    def __init__(self) -> None:
        self._goblins = []
        self.create_goblin()

    @property
    def goblins(self) -> List[Goblin]:
        return self._goblins

    def create_goblin(self, vitesse=1, sante=3) -> None:
        self._goblins.append(Goblin(chemin=Chemin().get_path_points(), vitesse=vitesse, sante=sante))

    def move(self) -> None:
        for goblin in self._goblins:
            if goblin.is_alive():
                goblin.deplacer()
