import os
from enemy import enemy_class

class rat_enemy(enemy_class):
    def __init__(self):
        super().__init__(os.path.join('assets', 'scene1', 'rat.png'), 50, 5, (1330, 150))
    
    def AI_logic(self, enemy):
        return super().AI_logic(enemy, 1, 0.2, 1.5, 1.8)


class letter(enemy_class):
    def __init__(self, sprite_location):
        super().__init__(sprite_location)
        self._index = 0
        self._dialogs = [
            "You pick up a letter and it say:\nI know the location of your father's killer...",
            "Meet me at 17th street ChickTie Ave 7713.\nYour friendly comrade."
        ]

    def interact(self, text_box, event):
        interact_value = super().interact(self._dialogs, self._index , text_box, event)
        if interact_value == True:
            self._index += 1
        elif interact_value == None:
            text_box.set_alpha(0)