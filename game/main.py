import pygame, os, time
from player import player_class
from cursor import cursor
from utils import draw_text

def main():
    global mainscreen
    global mouse
    global player
    
    pygame.init()
    mainscreen = pygame.display.setmode((1600,900))
    pygame.display.set_caption("Circle of Violence")
    pygame.mouse.set_visible(False)

    player = player_class(100, 5)
    mouse = cursor()

#rat position (1330, 150)
#def load_scene1():
#    background = pygame.image.load(os.path.join('assets', 'scene1', 'background.png'))
#    background = background.convert()


def combat(enemy):
    attack_cooldown = 3
    text_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
    sprites = pygame.sprite.RenderPlain((player, enemy, mouse))
    player.update_location((500, 400))
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

            pygame.key.set_repeat(1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d: #defend
                current = time.time()
                timer = round(current - time_defending_start, 2)
                player.defend_time = timer if timer < 2 and timer > 0 else 2
                player.defending = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_d:
                time_defending_start = time.time()
                player.defend_time = 0
                player.defending = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a and player.state != 1: #attack
                if not cooldown:
                    player.attacking(enemy)
                    timer_attack = time.time()
                    cooldown = True

        if cooldown:
                    time_pass = time.time() - timer_attack
                    if time_pass >= attack_cooldown:
                        cooldown = False
                    else:
                        time_left = round(attack_cooldown - time_pass, 2)
                        draw_text(str(time_left), 20, 0, 0, 50, text_surface, player.rect.midbottom)

        #Ai_logic() here
        


        if player.state == 1:
            y = player.pos[1]
            g = 255 - (7 * player.dmg_taken if player.dmg_taken < 35 else 255)
            draw_text(f"-{player.dmg_taken}", 50, 0, 0, 50, text_surface, (player.pos[0], y), (255, g, 0))
        else:
            y = player.pos[1]
            
        if enemy.state == 1:
            y = enemy.pos[1]
            g = 255 - (7 * enemy.dmg_taken if enemy.dmg_taken < 35 else 255)
            draw_text(f"-{enemy.dmg_taken}", 50, 0, 0, 50, text_surface, (enemy.pos[0], y), (255, g, 0))
        else:
            y = enemy.pos[1]
        
        stats = f"Player:\nHealth: {player.health}\n\nEnemy:\nHealth: {enemy.health}"
        draw_text(stats, 35, 17, 10, 340, text_surface, (0, 0))
        

        sprites.update()
        
        mainscreen.blits(blit_sequence=((background, (0, 0)),(text_surface, (0, 0))))
        sprites.draw(mainscreen)
        text_surface.fill((0, 0, 0, 0))
        pygame.display.update()

    pygame.quit()