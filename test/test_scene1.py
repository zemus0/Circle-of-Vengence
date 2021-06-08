import pygame, os, sys, time
sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'game'))
os.chdir('../game')

from enemy import enemy_class
from player import player_class
from cursor import cursor
from entities import *

def main():
    global mainscreen
    global mouse
    global player

    pygame.init()
    mainscreen = pygame.display.set_mode((1600,900))
    pygame.display.set_caption("test scene")
    pygame.mouse.set_visible(False)
    
    
    mouse = cursor()
    player = player_class(100, 20)
    scene1()


def scene1():
    scene1_data = os.path.join('assets', 'scene1')
    background = pygame.image.load(os.path.join(scene1_data, 'background.png')).convert()
    text_box_original = pygame.image.load(os.path.join('assets', 'dialog box.png')).convert_alpha()
    text_box = text_box_original.copy()
    text_box.set_alpha(0)
    mainscreen.blit(background, (0, 0))
    pygame.display.flip()

    player.update_location((540, 530))
    rat = rat_enemy()
    rat.update_location((65, 750))
    jacket = jacket_class(os.path.join(scene1_data, 'jacket.png'))
    jacket.update_location((150, 270))
    letter = letter_class(os.path.join(scene1_data, 'letter.png'))
    letter.update_location((1415, 717))
    #door = door_class()
    interactables = [rat, jacket, letter]
    sprites = pygame.sprite.RenderPlain((rat, jacket, letter, player, mouse))

    clock = pygame.time.Clock()
    running = True
    quit_game = False
    interact = False
    finish_dialog = False
    while running:
        clock.tick(60)
        if not interact:
            collision = mouse.interact_check(interactables)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                quit_game = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if collision != -1 and not interact:
                    interact = True
                if interact:
                    text_box = text_box_original.copy()
                    finish_dialog = interactables[collision].interact(text_box, event)
                    if finish_dialog == True:
                        text_box = text_box_original.copy()
                        text_box.set_alpha(0)
                        interact = False
            


        #rat, jacket, letter
        if finish_dialog == True:
            if collision == 0:
                print("go to combat")
                #combat(interactables[collision])
                player.items['banana_bullet'] = True
            elif collision == 1:
                player.items['money'] = 50
            elif collision == 2:
                pass
                #make the door interactable
        
        
        
        sprites.update()
        player.movement()
        
        mainscreen.blits(((background, (0, 0)),(text_box, (0, 0))))
        sprites.draw(mainscreen)
        pygame.display.update()
    
    if quit_game:
        pygame.quit


if __name__ == "__main__":
    main()