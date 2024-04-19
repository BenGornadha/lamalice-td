from __future__ import annotations
from typing import List

from mobs.goblin import Goblin
from mobs.goblinfactory import GoblinFactory, Goblins


class AnnounceNewWave:
    def __eq__(self, other):
        return isinstance(other, AnnounceNewWave)


class Waves:

    def __init__(self):
        self._waves: List[Wave] = []
        self._current_wave: Wave | None = None
        self._current_index = 0

    @property
    def current_wave(self) -> Wave:
        return self._current_wave

    @property
    def current_index(self):
        return self._current_index

    def ennemies(self) -> List[Goblin]:
        return self.current_wave.enemies.goblins

    def move_ennemies(self) -> None:
        self.current_wave.move()

    def draw_ennemies(self) -> None:
        self.current_wave.draw()

    def register_wave(self, wave: Wave) -> None:
        self._waves.append(wave)
        if self._current_wave is None:
            self._current_wave = wave

    def _current_wave_is_over(self) -> bool:
        return self._current_wave.all_mobs_defeated()

    def _all_enemies_already_spawned(self) -> bool:
        return self._current_wave.all_enemies_spawned()

    def _spawn_mob(self, current_time: int) -> None:
        self._current_wave.spawn_mob(current_time=current_time)

    def run(self, current_time: int):
        if not self._all_enemies_already_spawned():
            print("spawning mob")
            self._spawn_mob(current_time=current_time)
            return
        if self._current_wave_is_over():
            if self._current_index + 1 < len(self._waves):
                self.increment_wave()
                return AnnounceNewWave()
            return


    def increment_wave(self):
        self._current_index += 1
        self._current_wave = self._waves[self._current_index]


class Wave:
    def __init__(self, goblin_factory: GoblinFactory, enemy_hp: int = 2, num_enemies=30):
        self.goblin_factory = goblin_factory
        self.enemy_hp = enemy_hp
        self.num_enemies = num_enemies
        self.spawned_enemies = 0
        self.last_spawn_time = 0
        self.enemies = Goblins()

    def spawn_mob(self, current_time: int) -> None:
        if self.spawned_enemies < self.num_enemies:
            if current_time - self.last_spawn_time > 1000:  # Une seconde entre chaque ennemi
                self.enemies.add_goblin(self.goblin_factory.create_goblin(vitesse=1, sante=self.enemy_hp))
                self.spawned_enemies += 1
                self.last_spawn_time = current_time

    def all_enemies_spawned(self) -> bool:
        return self.spawned_enemies == self.num_enemies

    def all_mobs_defeated(self) -> bool:
        return all(goblin.is_dead() for goblin in self.enemies.goblins)

    def move(self) -> None:
        for goblin in self.enemies.goblins:
            if goblin.is_alive():
                goblin.deplacer()

    def draw(self):
        for goblin in self.enemies.goblins:
            goblin.draw()
