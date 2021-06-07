import pygame, os, sys, math
class player_class(pygame.sprite.Sprite):
    def __init__(self, health, attack_power):
        super().__init__()
        self._player_state = [os.path.join('assets', 'player', 'normal_player.png'), 
                            os.path.join('assets', 'player', 'damaged_player.png'),
                            os.path.join('assets', 'player', 'attacking_player.png')]
        
        self._attack_power = attack_power
        self._dir = 0 #0 for left, 1 for right
        self._state = 0
        self._frame = 0
        self.health = health
        self._defending = False
        self._defend_time = 0.1

        self.image = pygame.image.load(self._player_state[0]).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.image.get_rect()

    def update(self):
        if self._state == 2: # 2 for attacking
            move_dist = 10
            if self._frame <= 15:
                self.rect = self.rect.move((move_dist, -move_dist))
            elif self._frame <= 30:
                self.rect = self.rect.move((-move_dist, move_dist))
            else:
                self.change_state(0)
                self._frame = 0
            self._frame += 1
        elif self._state == 1: # 1 for damaged
            move_dist = 2
            if self._frame <= 5:
                self.rect = self.rect.move((-move_dist, move_dist))
            elif self._frame <= 10:
                self.rect = self.rect.move((move_dist, -move_dist))
            else:
                self.change_state(0)
                self._frame = 0
            self._frame += 1

    def take_damage(self, dmg):
        self.change_state(1)
        if self._defending:
            dmg = math.floor(dmg/(2/self._defend_time))
            self.health -= dmg
        else:
            self.health -= dmg


    def attacking(self, target):
        self.change_state(2)
        target.take_damage(self._attack_power)


    def change_state(self, state_int):
        self.image = pygame.image.load(self._player_state[state_int]).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self._state = state_int

    def movement(self):
        keys = pygame.key.get_pressed()
        speed = 10
        if keys[pygame.K_d]: # right key
            if not self._dir: 
                self.image = pygame.transform.flip(self.image, 1, 0)
                self._dir = 1
            self.rect = self.rect.move((speed, 0))
        elif keys[pygame.K_a]: # left key
            if self._dir:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self._dir = 0
            self.rect = self.rect.move((-speed, 0))

    def update_location(self, x, y):
        self.rect.move_ip(x, y)