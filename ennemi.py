class Ennemi:
    def __init__(self, chemin, vitesse=1, sante=100):
        """
        Initialise un nouvel ennemi.

        :param chemin: Une liste de tuples représentant les points du chemin que l'ennemi suivra.
        :param vitesse: La vitesse à laquelle l'ennemi se déplace le long du chemin.
        :param sante: La santé initiale de l'ennemi.
        """
        self._chemin = chemin
        self._vitesse = vitesse
        self._sante = sante
        self._position_index = 0  # Indice du point actuel sur le chemin
        self._position = chemin[0]  # Position initiale de l'ennemi

    @property
    def position(self) -> tuple:
        return self._position

    def deplacer(self):
        """
        Déplace l'ennemi le long du chemin.
        """
        # Incrémente l'index de position à la vitesse de l'ennemi.
        # Assure-toi de ne pas dépasser la longueur du chemin.
        # Vérifie si l'ennemi a atteint ou dépassé la fin du chemin
        self._position_index += self._vitesse
        if self._position_index >= len(self._chemin):
            self._position_index = 0  # Remet l'ennemi au début du chemin

        self._position = self._chemin[self._position_index]

    def subir_degats(self, degats):
        """
        Applique des dégâts à l'ennemi.

        :param degats: La quantité de dégâts infligés à l'ennemi.
        """
        self._sante -= degats
        if self._sante <= 0:
            self.mourir()

    def mourir(self):
        """
        Gère la mort de l'ennemi.
        """
        print("L'ennemi est mort!")
