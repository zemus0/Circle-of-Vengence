import pygame
import os, sys
class player(pygame.sprite.Sprite):
    def __init__(self, health, stamina, bullets):
        super().__init__()
        self.player_state = [os.path.join('assets', 'player', 'normal_player.png'), 
                            os.path.join('assets', 'player', 'damaged_player.png'),
                            os.path.join('assets', 'player', 'attacking_player.png')]
        self.taking_dmg_moveset = [] #to be fill in with int
        self.attacking_moveset = [] #to be fill in with int
        self.attack_state = False
        self.damaged_state = False
        self.health = health
        self.stamina = stamina
        self.bullets = bullets
        self.dir = 0 #0 for left, 1 for right
        self.change_state(0)

    #if attackin move player up a bit
    #if takin dmg move player down a bit
    #self.rect.move((x,y))
    def update(self):
        if self.attack_state:
            pass
        elif self.damaged_state:
            pass

    #check mouse position, left click to interact.
    def interact(self, target):
        target.interact_w_player()

    def take_damage(self, dmg):
        self.change_state(1)
        self.damaged_state = True
        self.health -= dmg

    def attacking(self, target, weapon):
        self.change_state(2)
        self.attack_state = True
        self.stamina -= weapon.stamina_cost
        dmg = weapon.strength - target.defense
        target.take_damage(dmg)

    def change_state(self, state_int):
        self.image = pygame.image.load(self.player_state[state_int]).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.image.get_rect()

    def movement(self):
        keys = pygame.key.get_pressed()
        speed = 10
        if keys[pygame.K_d]: # right key
            if not self.dir: 
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.dir = 1
            self.rect = self.rect.move((speed, 0))
        elif keys[pygame.K_a]: # left key
            if self.dir:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.dir = 0
            self.rect = self.rect.move((-speed, 0))
    
    def update_location(self, x, y):
        self.rect.move_ip(x, y)