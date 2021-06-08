import os
from enemy import enemy_class

class rat_enemy(enemy_class):
    def __init__(self):
        super().__init__(os.path.join('assets', 'scene1', 'rat.png'), 50, 5, (1330, 150))
    
    def AI_logic(self, enemy):
        return super().AI_logic(enemy, 1, 0.2, 1.5, 1.8)