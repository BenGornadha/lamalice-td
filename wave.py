from mobs.goblins import Goblins


class Wave:
    def __init__(self, goblin_factory: Goblins, enemy_hp: int = 2, num_enemies=30):
        self.goblin_factory = goblin_factory
        self.enemy_hp = enemy_hp
        self.num_enemies = num_enemies
        self.spawned_enemies = 0
        self.last_spawn_time = 0
        self.enemies = []



    def spawn_mob(self, current_time: int) -> None:
        if self.spawned_enemies < self.num_enemies:
            if current_time - self.last_spawn_time > 1000:  # Une seconde entre chaque ennemi
                self.goblin_factory.create_goblin(vitesse=1, sante=self.enemy_hp)
                self.spawned_enemies += 1
                self.last_spawn_time = current_time

    def all_enemies_spawned(self) -> bool:
        return self.spawned_enemies == self.num_enemies

    def all_mobs_defeated(self) -> bool:
        return all( goblin.is_dead() for goblin in self.enemies)
