import pygame, os, sys, time
sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'game'))
os.chdir('../game')

from player import player_class
from cursor import cursor
from enemy import enemy_class
from utils import draw_text



def main():
    global mainscreen
    global mouse
    global player

    pygame.init()
    mainscreen = pygame.display.set_mode((1600,900))
    pygame.display.set_caption("test combat")
    pygame.mouse.set_visible(False)
    
    
    player = player_class(100, 20)
    mouse = cursor()
    rat = enemy_class(100, 10, (1330, 150), os.path.join('assets', 'scene1', 'rat.png'))

    combat(rat)


def combat(enemy):
    text_surface = pygame.Surface((340, 235))
    sprites = pygame.sprite.RenderPlain((player, enemy, mouse))
    player.update_location(500, 400)
    enemy.update_location(enemy.combat_coord)

    clock = pygame.time.Clock()
    background = pygame.image.load(os.path.join('assets','battle scene.png')).convert()
    mainscreen.blit(background, (0, 0))
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d: #defend
                timer = round(time.time() - time_defending_start, 2)
                player.defend_time = timer if timer < 2 and timer > 0 else 2
                player.defending = True
            elif not (event.type == pygame.KEYDOWN and event.key == pygame.K_d):
                time_defending_start = time.time()
                player.defend_time = 0
                player.defending = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a: #attack
                if not cooldown:
                    player.attacking(enemy)
                    timer_attack = time.time()
                    cooldown = True
                if cooldown and  time.time() - timer_attack >= 5:
                    cooldown = False
                    #add some sort of cool down graphics


        stats = f"Player:\nHealth: {player.health}\n\nEnemy:\nHealth: {enemy.health}"
        draw_text(stats, 35, 17, 10, text_surface, (0, 0))

        sprites.update()

        mainscreen.blits(blit_sequence=((background, (0, 0)),(text_surface, (0, 0))))
        sprites.draw(mainscreen)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()