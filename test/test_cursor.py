import pygame
import os, sys

os.chdir('../game')

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
        self.dir = 1 # 0 for left, 1 for right
        self.change_state(0)

    #if attackin move player up a bit
    #if takin dmg move player down a bit
    #self.rect.move((x,y))
    def update(self):
        if self.attack_state:
            print("attackin")
            self.attack_state = False
        elif self.damaged_state:
            print("damages")
            self.damaged_state = False

    #check mouse position, left click to interact.
    def interact(self, target):
        target.interact_w_player()

    def take_damage(self, dmg):
        self.change_state(1)
        self.damaged_state = True
        self.health -= dmg

    def attacking(self):
        self.change_state(2)
        self.attack_state = True

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
        elif keys[pygame.K_1]:
            self.attacking()

    def update_location(self, x, y):
        self.rect.move_ip(x, y)

class cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'cursor_normal.png')).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, interactables):
        collide_check = self.rect.collidelist(interactables)
        if collide_check != -1:
            self.image = pygame.image.load(os.path.join('assets', 'cursor_selectable.png')).convert_alpha()
            #self.rect = self.image.get_rect()
        else:
            self.image = pygame.image.load(os.path.join('assets', 'cursor_normal.png')).convert_alpha()
        mouse_pos = pygame.mouse.get_pos()
        self.rect.midtop = mouse_pos
        return collide_check



def main():
    pygame.init()
    screen = pygame.display.set_mode((1600,900))
    pygame.display.set_caption("Test_Cursor")

    background = pygame.image.load(os.path.join('assets','scene1', 'background.png')).convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()

    user = player(10, 10, 10)
    mouse = cursor()
    sprites = pygame.sprite.RenderPlain((user, mouse))
    user.update_location(540, 530)
    clock = pygame.time.Clock()
    interactable = [user.rect]
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        #sprites.update()
        #only needed to be call when in combat
        user.movement()
        hit_index = mouse.update(interactable)
        if hit_index != -1:
            print("hit")
        

        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.update()

        

    
        
if __name__ == "__main__":
    main()
        