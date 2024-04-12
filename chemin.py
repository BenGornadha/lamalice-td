def generer_chemin_horizontal(y, x_debut, x_fin, pas):
    return [(x, y) for x in range(x_debut, x_fin + 1, pas)]


def generer_chemin_vertical(x, y_debut, y_fin, pas):
    return [(x, y) for y in range(y_debut, y_fin + 1, pas)]


# Exemple d'utilisation :
FIRST_PATH = generer_chemin_horizontal(325, 0, 130, 10)
SECOND_PATH = generer_chemin_vertical(130, 325, 145, -10)
THIRD_PATH = generer_chemin_horizontal(145, 130, 295, 10)
FOURTH_PATH = generer_chemin_vertical(295, 145, 395, 10)
FIFTH_PATH = generer_chemin_horizontal(395, 295, 505, 10)
SIX_PATH = generer_chemin_vertical(505, 395, 275, -10)
SEVENTH_PATH = generer_chemin_horizontal(275, 505, 800, 10)




class Chemin:
    def __init__(self):
        self.points =[(x,y) for x,y in FIRST_PATH] + [(x,y) for x,y in SECOND_PATH] + [(x,y) for x,y in THIRD_PATH] +  [(x,y) for x,y in FOURTH_PATH] +   [(x,y) for x,y in FIFTH_PATH] +  [(x,y) for x,y in SIX_PATH] + [(x,y) for x,y in SEVENTH_PATH]

    def get_path_points(self):
        # Retourne la liste des points du chemin
        return self.points

    def get_next_point(self, current_point):
        # Retourne le prochain point sur le chemin en se basant sur la position actuelle
        # Si l'ennemi est au dernier point, on peut le laisser à sa position ou le faire disparaître
        if current_point in self.points:
            current_index = self.points.index(current_point)
            if current_index < len(self.points) - 1:
                return self.points[current_index + 1]
        return current_point
