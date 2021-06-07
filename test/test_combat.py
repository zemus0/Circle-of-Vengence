import pygame, os, sys, time
sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'game'))
os.chdir('../game')

from enemy import enemy_class
from player import player_class
from cursor import cursor
from enemies import rat
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
    mouse = rat() 
    combat(mouse)


def combat(enemy):
    combat_end = False
    combat_animation_frame = 0
    attack_cooldown = 3
    text_surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
    sprites = pygame.sprite.RenderPlain((player, enemy, mouse))
    player.update_location((500, 400))
    enemy.update_location(enemy.combat_coord)

    clock = pygame.time.Clock()
    background = pygame.image.load(os.path.join('assets','battle scene.png')).convert()
    gameover = pygame.image.load(os.path.join('assets','you died.png')).convert()
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

            if not combat_end:
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
            elif player.state == 3:
                if event.type == pygame.KEYDOWN:
                    main()
                    running = False
                else:
                    running = True

        if cooldown:
            time_pass = time.time() - timer_attack
            if time_pass >= attack_cooldown:
                cooldown = False
            else:
                time_left = round(attack_cooldown - time_pass, 2)
                draw_text(str(time_left), 20, 0, 0, 50, text_surface, player.rect.midbottom)

        enemy.AI_logic(player)

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

        #death check
        if player.health <= 0:
            player.death()
            combat_end = True
            player.rotation += 2 if player.rotation < 90 else 0
            combat_animation_frame += 1
            player.image = pygame.transform.rotate(player.original, player.rotation)
            if combat_animation_frame >= 60:
                mainscreen.blit(gameover, (0, 0))
                
        elif enemy.health <= 0:
            enemy.death()
            combat_end = True
            enemy.rotation += 2 if enemy.rotation < 90 else 0
            combat_animation_frame += 1
            enemy.image = pygame.transform.rotate(enemy.original, enemy.rotation)
            if combat_animation_frame >= 120:
                running = False

        pygame.display.update()

    if not combat_end:
        pygame.quit()

if __name__ == "__main__":
    main()