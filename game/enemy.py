import pygame, os, sys, math
class enemy_class(pygame.sprite.Sprite):
    def __init__(self, health, attack_power, combat_coord, sprite_location):
        super().__init__()
        self._attack_power = attack_power
        self._frame = 0

        self.image = pygame.image.load(sprite_location).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.pos = self.rect.midtop
        self.state = 0 #2 attackin, 1 taking dmg
        self.defending = False
        self.defend_time = 0.1
        self.health = health
        self.combat_coord = combat_coord
        self.dmg_taken = 0


    def update(self):
        if self.state == 1: # 1 for damaged
            move_dist = 2
            if self._frame <= 5:
                self.rect = self.rect.move((move_dist, -move_dist))
            elif self._frame <= 10:
                self.rect = self.rect.move((-move_dist, move_dist))
            elif self._frame <= 30:
                self.state = 0
                self._frame = 0
                self.update_location(self.combat_coord)
            self._frame += 1
        elif self.state == 2: # 2 for attacking
            move_dist = 10
            if self._frame <= 15:
                self.rect = self.rect.move((-move_dist, move_dist))
            elif self._frame <= 30:
                self.rect = self.rect.move((move_dist, -move_dist))
            else:
                self.state = 0
                self._frame = 0
                self.update_location(self.combat_coord)
            self._frame += 1

    def take_damage(self, dmg):
        self.state = 1
        if self.defending:
            dmg = math.floor(dmg/(2/self.defend_time))
            
        self.dmg_taken = dmg
        self.health -= dmg

    def attacking(self, target):
        self.state = 2
        target.take_damage(self._attack_power)

    def AI_logic(self):
        #add AI
        pass

    def update_location(self, coord):
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        self.pos = self.rect.center[0], self.rect.center[1] - self.rect.h