import pygame, os, sys

class cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'cursor_normal.png')).convert_alpha()
        self.rect = self.image.get_rect()

    def interact_check(self, interactables):
        collide_check = self.rect.collidelist(interactables)
        if collide_check != -1:
            self.image = pygame.image.load(os.path.join('assets', 'cursor_selectable.png')).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join('assets', 'cursor_normal.png')).convert_alpha()
        return collide_check
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.midtop = mouse_pos