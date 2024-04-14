from typing import List

from arrow import Arrow
from building import Building
from goblin import Goblin


class Tour(Building):
    def __init__(self, position: tuple, range: int, damage: int):
        self._position = position
        self._portee = range
        self._damage = damage
        self._level = 0
        self._last_attack_time = 0
        self._attack_cooldown = 400
        self.arrow = Arrow()

    def attack(self, current_time: int, ennemis: List[Goblin]) -> None:
        self._current_arrow(current_time=current_time)
        if not self._can_attack(current_time=current_time):
            return
        target = self._trouver_ennemi_le_plus_proche_de_la_sortie(ennemis=ennemis)
        if target is None:
            return
        self._launch_new_arrow(current_time=current_time, to=target)

    def _current_arrow(self, current_time: int):
        if self.arrow.is_already_launch():
            self.arrow.animation(current_pygame_time=current_time, last_attack_time=self._last_attack_time)

            if self.arrow.has_reach_mob():
                self.arrow.target.subir_degats(self._damage)
                self.arrow.reset_position()
                self.arrow.reset_target()

    def _trouver_ennemi_le_plus_proche_de_la_sortie(self, ennemis: List[Goblin]) -> Goblin | None:
        ennemis_a_portee = [ennemi for ennemi in ennemis if self._ennemi_a_portee(ennemi)]
        if ennemis_a_portee:
            return min(ennemis_a_portee, key=lambda ennemi: self._compute_distance_to_exit(ennemi.position))

    def _ennemi_a_portee(self, ennemi: Goblin) -> bool:
        distance = self._compute_distance_for(position=ennemi.position)
        if distance:
            return distance <= self._portee
        return False

    def _launch_new_arrow(self, current_time: int, to: Goblin):
        self.arrow.set_position(x=self.position[0], y=self.position[1])
        self._last_attack_time = current_time
        self.arrow.lock_target(mob=to)
