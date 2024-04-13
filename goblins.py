from chemin import Chemin
from goblin import Goblin


class Goblins:
    def __init__(self):
        self._goblins = []
        self.create_goblin()

    @property
    def goblins(self):
        return self._goblins

    def create_goblin(self) -> None:
        self._goblins.append(Goblin(chemin=Chemin().get_path_points(),vitesse=1,sante=3))

    def move(self):
        for goblin in self._goblins:
            if goblin.is_alive():
                goblin.deplacer()
