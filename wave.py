from __future__ import annotations
from typing import List

from pygame import Surface

from interface.image_repository import ImageRepository
from mobs.goblin import Goblin
from mobs.goblinfactory import GoblinFactory, Goblins


class AnnounceNewWave:
    def __eq__(self, other):
        return isinstance(other, AnnounceNewWave)


class Waves:

    def __init__(self, screen: Surface, image_repository: ImageRepository):
        self._waves: List[Wave] = []
        self.goblins_factory = GoblinFactory(screen=screen, image=image_repository.surface("mob"))
        self._current_index = 0
        self._current_wave: Wave = Wave(self.goblins_factory, hp=200, num_enemies=5, vitesse=2, spawn_timelapse=1000)
        self._register_waves()

    def _register_waves(self):
        previous_wave = self.current_wave
        for i in range(1, 100):
            if i % 5 == 0:
                wave = Wave(goblin_factory=self.goblins_factory, hp=previous_wave.hp * 1.1,
                            num_enemies=previous_wave.num_enemies + 3, vitesse=previous_wave.speed * 2, spawn_timelapse=previous_wave.spawn_timelapse *0.9)
            else:
                wave = Wave(goblin_factory=self.goblins_factory, hp=previous_wave.hp * 1.1,
                            num_enemies=previous_wave.num_enemies + 1, vitesse=previous_wave.speed)
            self.register_wave(wave=wave)
            previous_wave = wave

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
    def __init__(self, goblin_factory: GoblinFactory, hp: float = 2, num_enemies=30, vitesse=1,spawn_timelapse : float = 1000):
        self.goblin_factory = goblin_factory
        self.hp = hp
        self.num_enemies = num_enemies
        self.spawned_enemies = 0
        self.spawn_timelapse = spawn_timelapse
        self.last_spawn_time = 0
        self.enemies = Goblins()
        self.speed = vitesse

    def spawn_mob(self, current_time: int) -> None:
        if self.spawned_enemies < self.num_enemies:
            if current_time - self.last_spawn_time > self.spawn_timelapse:  # Une seconde entre chaque ennemi
                self.enemies.add_goblin(self.goblin_factory.create_goblin(vitesse=self.speed, sante=self.hp))
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
