class Goblin:
    def __init__(self, chemin, vitesse=1, sante=2):
        self._chemin = chemin
        self._vitesse = vitesse
        self._sante = sante
        self._position_index = 0
        self._position = chemin[0]

    def is_alive(self) -> bool:
        return self._sante > 0

    def is_dead(self):
        return self._sante <= 0

    @property
    def position(self) -> tuple:
        return self._position

    def deplacer(self):
        self._position_index += self._vitesse
        if self._position_index >= len(self._chemin):
            self._position_index = 0  # Remet l'ennemi au début du chemin

        self._position = self._chemin[self._position_index]

    def subir_degats(self, degats):
        self._sante -= degats
        if self._sante <= 0:
            self.mourir()

    def mourir(self):
        self._position = None

