from ennemi import Ennemi


class Tour:
    def __init__(self, position: tuple, portee: int, degats: int):
        """
        Initialise une nouvelle tour.

        :param position: Un tuple (x, y) représentant la position de la tour sur le plateau.
        :param portee: Un entier indiquant la portée d'attaque de la tour (distance à laquelle elle peut attaquer les ennemis).
        :param degats: Les dégâts infligés par la tour à chaque attaque.
        """
        self._position = position
        self._portee = portee
        self._degats = degats

    @property
    def position(self):
        return self._position

    def _ennemi_a_portee(self, ennemi: Ennemi):
        """
        Vérifie si un ennemi est à portée de la tour.

        :param ennemi: L'ennemi à vérifier.
        :return: True si l'ennemi est à portée, False sinon.
        """
        ennemi_position = ennemi._position
        distance = ((self._position[0] - ennemi_position[0]) ** 2 + (
                    self._position[1] - ennemi_position[1]) ** 2) ** 0.5
        return distance <= self._portee

    def attaquer(self, ennemi: Ennemi):
        """
        Inflige des dégâts à un ennemi si celui-ci est à portée.

        :param ennemi: L'ennemi à attaquer.
        """
        if self._ennemi_a_portee(ennemi=ennemi):
            ennemi.subir_degats(self._degats)
