import pygame, os, sys, math
class player_class(pygame.sprite.Sprite):
    def __init__(self, health, attack_power):
        super().__init__()
        self._player_state = [os.path.join('assets', 'player', 'normal_player.png'), 
                            os.path.join('assets', 'player', 'damaged_player.png'),
                            os.path.join('assets', 'player', 'attacking_player.png')]
        
        self._attack_power = attack_power
        self._dir = 1 #0 for left, 1 for right
        self._frame = 0
        self._mid_animation = False
        self.items = {}
        self.state = 0
        self.dmg_taken = 0
        self.health = health
        self.defending = False
        self.defend_time = 0.1
        
        self.image = pygame.image.load(self._player_state[0]).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.pos = self.rect.midtop
        self.combat_coord = 500, 400
        self.last_coord = 0, 0

    def update(self):
        if self.state == 2: # 2 for attacking
            self._mid_animation = True
            move_dist = 10
            if self._frame <= 15:
                self.rect = self.rect.move((move_dist, -move_dist))
            elif self._frame <= 30:
                self.rect = self.rect.move((-move_dist, move_dist))
            else:
                self._mid_animation = False
                self.change_state(0)
                self._frame = 0
                self.update_location(self.combat_coord)
            self._frame += 1
        elif self.state == 1: # 1 for damaged
            self._mid_animation = True
            move_dist = 2
            if self._frame <= 5:
                self.rect = self.rect.move((-move_dist, move_dist))
            elif self._frame <= 10:
                self.rect = self.rect.move((move_dist, -move_dist))
            elif self._frame <= 30:
                self._mid_animation = False
                self.change_state(0)
                self._frame = 0
                self.update_location(self.combat_coord)
            self._frame += 1


    def take_damage(self, dmg):
        self.change_state(1)
        if self.defending:
            dmg = math.floor(dmg/(2/self.defend_time))
            
        self.health -= dmg
        self.dmg_taken = dmg

    def death(self):
        self.state = 3
        self.rotation = 0
        self.original = self.image

    def attacking(self, target):
        self.change_state(2)
        target.take_damage(self._attack_power)


    def change_state(self, state_int):
        self.image = pygame.image.load(self._player_state[state_int]).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        if not self._mid_animation:
            self.state = state_int

    def movement(self, mainscreen):
        keys = pygame.key.get_pressed()
        width = mainscreen.get_width()
        speed = 10
        if keys[pygame.K_d] and self.rect.midright[0] + speed < width: # right key
            if not self._dir: 
                self.image = pygame.transform.flip(self.image, 1, 0)
                self._dir = 1
            self.rect = self.rect.move((speed, 0))
        elif keys[pygame.K_a] and self.rect.midleft[0] - speed > 0: # left key
            if self._dir:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self._dir = 0
            self.rect = self.rect.move((-speed, 0))

    def update_location(self, coord):
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        self.pos = self.rect.center[0], self.rect.center[1] - self.rect.h
        self._dir = 1