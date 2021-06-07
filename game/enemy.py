import pygame, os, sys, math
class enemy(pygame.sprite.Sprite):
    def __init__(self, health, attack_power):
        super().__init__()
        self._attack_power = attack_power
        self._state = 0 #0 attackin, 0 taking dmg
        self._frame = 0
        self.health = health
        self.defending = False
        self.defend_time = 0.1

    def update(self):
        if self._state == 2:
            if self._frame <= 5:
                self.rect.move(5, -5)
            elif self._frame <= 10:
                self.rect.move(-5, 5)
            else:
                self._state = 0
                self._frame = 0
            self._frame += 1
        elif self._state == 1:
            if self._frame <= 5:
                self.rect.move(-5, 5)
            elif self._frame <= 10:
                self.rect.move(5, -5)
            else:
                self._state = 0 
                self._frame = 0
            self._frame += 1

    def take_damage(self, dmg):
        self._state = 1
        if self._defending:
            dmg = math.floor(dmg/(2/self._defend_time))
            self.health -= dmg
        else:
            self.health -= dmg

    def attacking(self, target):
        self._state = 0
        target.take_damage(self._attack_power)

    def AI_logic(self):
        #add AI
        pass

    def update_location(self, x, y):
        self.rect.move_ip(x, y)