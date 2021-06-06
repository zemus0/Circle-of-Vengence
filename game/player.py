import pygame, os, sys
class player(pygame.sprite.Sprite):
    def __init__(self, health):
        super().__init__()
        self._player_state = [os.path.join('assets', 'player', 'normal_player.png'), 
                            os.path.join('assets', 'player', 'damaged_player.png'),
                            os.path.join('assets', 'player', 'attacking_player.png')]
        self._attack_state = False
        self._damaged_state = False
        self.health = health
        self.defending = False
        self._dir = 0 #0 for left, 1 for right
        self.change_state(0)

    #if attackin move player up a bit
    #if takin dmg move player down a bit
    #self.rect.move((x,y))
    def update(self):
        if self._attack_state:
            pass
        elif self._damaged_state:
            pass

    def take_damage(self, dmg, defend):
        self.change_state(1)
        self._damaged_state = True
        if self.defending:
            self.health -= dmg/2
        else:
            self.health -= dmg


    def attacking(self, target, dmg):
        self.change_state(2)
        self._attack_state = True
        target.take_damage(dmg)


    def change_state(self, state_int):
        self.image = pygame.image.load(self._player_state[state_int]).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.image.get_rect()

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