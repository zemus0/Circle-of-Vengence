import pygame, os, sys

class cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'cursor_normal.png')).convert_alpha()
        self.rect = self.image.get_rect()

    def interact_check(self, interactables):
        interactables_items = []
        interactables_key = []
        for key, item in interactables.items():
            if item is not None:
                interactables_items.append(item)
                interactables_key.append(key)

        collide_check = self.rect.collidelist(interactables_items)

        if collide_check != -1:
            self.image = pygame.image.load(os.path.join('assets', 'cursor_selectable.png')).convert_alpha()
            return_val = str(interactables_key[collide_check])
        else:
            self.image = pygame.image.load(os.path.join('assets', 'cursor_normal.png')).convert_alpha()
            return_val = -1
            
        return return_val
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.midtop = mouse_pos