import os, pygame
from enemy import enemy_class
from utils import draw_text

class rat_enemy(enemy_class):
    def __init__(self):
        super().__init__(os.path.join('assets', 'scene1', 'rat.png'), 50, 5, (1330, 150))
        self._index = -1
        self._dialogs = [
            "You saw a rat chewing on something...",
            "It hisses at you and charging in for the attack."
        ]


    def AI_logic(self, enemy):
        return super().AI_logic(enemy, 1, 0.2, 1.5, 1.8)

    def interact(self, text_box):
        return super().interact(self._dialogs, text_box)


class letter_class(enemy_class):
    def __init__(self, sprite_location):
        super().__init__(sprite_location)
        self._index = -1
        self._dialogs = [
            "You pick up a letter and it say:\nI know the location of your father's killer...",
            "Meet me at 17th street ChickTie Ave 7713.\nYour friendly comrade."
        ]

    def interact(self, text_box):
        return super().interact(self._dialogs, text_box)
        
class jacket_class(enemy_class):
    def __init__(self, sprite_location):
        super().__init__(sprite_location, alpha=True)
        self._index = -1
        self._dialogs = [
            "You search through the pocket of your jacket and found...",
            "50 bucks."
        ]

    def interact(self, text_box):
        return super().interact(self._dialogs, text_box)

        
        