class Building:
    _position = None
    _last_attack_time = 0
    _attack_cooldown = 0
    _damage = 0

    @property
    def position(self) -> tuple:
        return self._position

    def _can_attack(self, current_time: int) -> bool:
        return current_time - self._last_attack_time > self._attack_cooldown

    def _compute_distance_for(self, position: tuple) -> int:
        if position:
            return ((self._position[0] - position[0]) ** 2 + (self._position[1] - position[1]) ** 2) ** 0.5

    def _compute_distance_to_exit(self, point1):
        return ((point1[0] - 800) ** 2 + (point1[1] - 235) ** 2) ** 0.5

    def lvp_up(self):
        self._attack_cooldown = self._attack_cooldown * 0.95
        self._damage = self._damage * 1.05
