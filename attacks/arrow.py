from typing import List

import pygame

from mobs.goblin import Goblin


class Arrow:
    def __init__(self):
        self._position: List | None = None
        self._target: Goblin | None = None
        self._speed = 500

    @property
    def position(self):
        return self._position

    @property
    def target(self) -> Goblin | None:
        return self._target

    def set_position(self, x: int, y: int) -> None:
        self._position = [x, y]

    def reset_position(self) -> None:
        self._position = None

    def reset_target(self) -> None:
        self._target = None

    def lock_target(self, mob: Goblin) -> None:
        self._target = mob

    def is_already_launch(self) -> bool:
        return self._position is not None

    def animation(self, current_pygame_time: int, last_attack_time: int) -> None:
        if self._target.is_dead():
            return
        direction = pygame.math.Vector2(self._target.position) - pygame.math.Vector2(self.position)
        if direction.length() > 0:
            direction = direction.normalize()
        self._position[0] += direction.x * self._speed * (current_pygame_time - last_attack_time) / 1000.0
        self._position[1] += direction.y * self._speed * (current_pygame_time - last_attack_time) / 1000.0

    def has_reach_mob(self) -> bool:
        return pygame.math.Vector2(self.position).distance_to(self._target.position) < 25
