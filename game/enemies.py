import os
from enemy import enemy_class

class rat(enemy_class):
    def __init__(self):
        super().__init__(50, 5, (1330, 150), os.path.join('assets', 'scene1', 'rat.png'))
    
    def AI_logic(self, enemy):
        return super().AI_logic(enemy, 1, 0.1, 1.5, 1.8)