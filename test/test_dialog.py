import pygame, os, sys, time
sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'game'))
os.chdir('../game')

from player import player_class
from cursor import cursor
from enemies import rat_enemy
from utils import (draw_text, dialog)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1600,900))
    pygame.display.set_caption("Test_Dialog")

    background = pygame.image.load(os.path.join('assets','scene1', 'background.png')).convert()
    text_box = pygame.image.load(os.path.join('assets', 'dialog box.png')).convert_alpha()
    text_box.set_alpha(0)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    player = player_class(10, 10)
    sprites = pygame.sprite.RenderPlain((player))
    player.update_location((540, 530))
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        dialog("testing testing 123\n aaaaaaaa", text_box)

        player.movement()

        screen.blits(((background, (0, 0)), (text_box, (0, 0))))
        sprites.draw(screen)
        pygame.display.update()

        

    
        
if __name__ == "__main__":
    main()