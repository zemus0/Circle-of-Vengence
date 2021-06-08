import pygame, os, time
from player import player_class
from cursor import cursor
from utils import draw_text
from entities import *

def play():
    global mainscreen
    global text_box_original
    global player
    global mouse
    
    pygame.init()
    mainscreen = pygame.display.setmode((1600,900))
    pygame.display.set_caption("Circle of Violence")
    pygame.mouse.set_visible(False)


    text_box_original = pygame.image.load(os.path.join('assets', 'dialog box.png')).convert_alpha()
    player = player_class(100, 5)
    mouse = cursor()

    do_player_died = scene1()

def scene1():
    scene1_data = os.path.join('assets', 'scene1')
    background = pygame.image.load(os.path.join(scene1_data, 'background.png')).convert()
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
    door = door_class()
    door.update_location
    interactables = [rat, jacket, letter]
    sprites = pygame.sprite.RenderPlain((rat, jacket, letter, door, player, mouse))

    clock = pygame.time.Clock()
    running = True
    quit_game = False
    interact = False
    finish_dialog = False
    while running:
        clock.tick(60)
        print(clock.get_fps())
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
                    finish_dialog = interactables[collision].interact(text_box)
                    if finish_dialog:
                        text_box = text_box_original.copy()
                        text_box.set_alpha(0)
                        interact = False

            if finish_dialog == 'e':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    return False

        #rat, jacket, letter
        if finish_dialog:
            if collision == 0:
                original_pos = player.rect.center
                ded = combat(interactables[collision])
                if ded:
                    return True
                #remove rat from rendering
                player.rect.center = original_pos
                player.items['banana_bullet'] = True
                text_box.set_alpha(255)
                draw_text("You recieved a banana bullet!!!", 45, 55, 55, 1490, text_box, (0, 0))
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
        return None   


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
                    return True

        if cooldown:
            time_pass = time.time() - timer_attack
            if time_pass >= attack_cooldown:
                cooldown = False
            else:
                time_left = round(attack_cooldown - time_pass, 2)
                draw_text(str(time_left), 20, 0, 0, 50, text_surface, player.rect.midbottom)

        if enemy.state != 3:
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
                return False

        pygame.display.update()

    if not combat_end:
        return None


def main():
    pygame.init()
    quit_game = False
    while True:
        quit_game = play()
        if quit_game == None:
            break

    pygame.quit()

