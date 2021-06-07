import pygame, os, sys, time, math
from .player import player
from .cursor import cursor

#global variables
interactable = []
user = player(100, 20)
mouse = cursor()

def main():
    pygame.init()
    mainscreen = pygame.display.setmode((1600,900))
    mainscreen.display.set_caption("Circle of Violence")


#def load_scene1():
#    background = pygame.image.load(os.path.join('assets', 'scene1', 'background.png'))
#    background = background.convert()


def combat(screen, enemy):
    sprites = pygame.sprite.RenderPlain((user, enemy))
    user.update_location(560, 460)
    enemy.update_location(1280, 90)

    clock = pygame.time.Clock()
    background = pygame.image.load(os.path.join('assets','battle scene.png')).convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()

    cooldown = False
    time_defending_start = time.time()
    timer_attack = time.time()
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.KEYDOWN and event.type == pygame.K_d: #defend 
                timer = round(time.time() - time_defending_start, 2)
                user.defend_time = timer if timer < 2 and timer > 0 else 2
                user.defending = True
            elif not (event.type == pygame.KEYDOWN and event.type == pygame.K_d):
                time_defending_start = time.time()
                user.defend_time = 0
                user.defending = False
            if event.type == pygame.KEYDOWN and event.type == pygame.K_a: #attack
                if not cooldown:
                    user.attacking(enemy)
                    timer = math.floor(time.time())
                    cooldown = True
                if cooldown and timer_attack - math.floor(time.time()) >= 5:
                    cooldown = False
                    #add some sort of cool down graphics


        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.update()
    
    pygame.quit()