import pygame, os, sys, time
from player import player_class
from cursor import cursor
from utils import draw_text
from enemy import enemy_class
from entities import *

def credit_scene():
    background = pygame.image.load(os.path.join('assets', 'credit.png')).convert()
    mainscreen.blit(background, (0, 0))
    pygame.display.flip()
    
    sprites = pygame.sprite.RenderPlain([mouse])

    clock = pygame.time.Clock()
    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None


        mainscreen.blit(background, (0, 0))
        sprites.draw(mainscreen)
        pygame.display.update()




def scene_final():
    scene3_data = os.path.join('assets', 'scene3')
    background = pygame.image.load(os.path.join(scene3_data, 'background.png')).convert()
    text_box = text_box_original.copy()
    text_box.set_alpha(0)
    mainscreen.blit(background, (0, 0))
    pygame.display.flip()

    player.update_location((175, 550))
    anti = antagonist_enemy()
    anti.update_location((775, 500))
    anti_son = antagonist_son()
    anti_son.update_location((1290, 655))
    interactables = {
        "anti": anti
    }

    sprites = pygame.sprite.RenderPlain([anti, player, mouse])

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
                    collide_with = collision
                    interact = True
                if interact:
                    text_box = text_box_original.copy()
                    finish_dialog = interactables[collide_with].interact(text_box)
                    if finish_dialog:
                        text_box = text_box_original.copy()
                        text_box.set_alpha(0)
                        interact = False



        #rat, jacket, letter, door
        if finish_dialog:
            if collide_with == "anti":
                original_pos = player.rect.x, player.rect.y
                anti_original_pos = anti.rect.x, anti.rect.y
                ded = combat(interactables[collide_with])
                if ded:
                    return True
                sprites.add(anti_son)
                interactables["anti"] = None
                interactables["anti_son"] = anti_son
                player.rect.x = original_pos[0]
                player.rect.y = original_pos[1]
                anti.rect.x = anti_original_pos[0]
                anti.rect.y = anti_original_pos[1]
            elif collide_with == "anti_son":
                return credit_scene

            finish_dialog = False
        
        sprites.update()
        player.movement(mainscreen)
        
        mainscreen.blits(((background, (0, 0)),(text_box, (0, 0))))
        sprites.draw(mainscreen)
        pygame.display.update()
    
    if quit_game:
        return None


def scene1(first_time=False):
    scene1_data = os.path.join('assets', 'scene1')
    background = pygame.image.load(os.path.join(scene1_data, 'background.png')).convert()
    text_box = text_box_original.copy()
    text_box.set_alpha(0)
    mainscreen.blit(background, (0, 0))
    pygame.display.flip()

    if first_time:
        player.update_location((540, 530))
    else:
        player.update_location(player.last_coord)

    jacket.update_location((150, 270))
    letter = letter_class()
    letter.update_location((1415, 700))
    door = door_class(os.path.join(scene1_data, 'door.png'))
    door.update_location((1300, 284))
    interactables = {
        "letter": letter
    }
    
    sprite_render = [jacket, letter, door, player, mouse]
    

    if rat.in_scene:
        interactables["rat"] = rat
        rat.update_location((65, 750))
        sprite_render.insert(0, rat)
    if jacket.in_scene:
        interactables["jacket"] = jacket

    sprites = pygame.sprite.RenderPlain(sprite_render)

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
                    collide_with = collision
                    interact = True
                if interact:
                    text_box = text_box_original.copy()
                    finish_dialog = interactables[collide_with].interact(text_box)
                    if finish_dialog:
                        text_box = text_box_original.copy()
                        text_box.set_alpha(0)
                        interact = False



        #rat, jacket, letter, door
        if finish_dialog:
            if collide_with == "rat":
                original_pos = player.rect.center
                ded = combat(interactables[collide_with])
                if ded:
                    return True
                sprites.remove(rat)
                interactables["rat"] = None
                player.rect.center = original_pos
                player.items['banana_bullet'] = True
            elif collide_with == "jacket":
                interactables["jacket"] = None
                player.items['money'] = 50   
            elif collide_with == "letter":
                interactables["door"] = door
            elif collide_with == "door":
                player.last_coord = (1333,530)
                return scene_final
            finish_dialog = False
        
        sprites.update()
        player.movement(mainscreen)
        
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
    defended = False
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
                    if not defended:
                        time_defending_start = time.time()
                    current = time.time()
                    timer = round(current - time_defending_start, 2)
                    player.defend_time = timer if timer < 2 and timer > 0 else 2
                    player.defending = True
                    defended = True
                elif event.type == pygame.KEYUP and event.key == pygame.K_d:
                    defended = False
                    player.defend_time = 0
                    player.defending = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_a: #attack
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
        
        

        if not combat_end:
            time_pass = enemy.AI_logic(player)
            enemy_cooldown = round(enemy.attack_cooldown - time_pass, 2)
            draw_text(str(enemy_cooldown), 20, 0, 0, 50, text_surface, enemy.rect.midbottom)

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
        
        mainscreen.blit(background, (0, 0))
        sprites.draw(mainscreen)
        mainscreen.blit(text_surface, (0, 0))
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
            if combat_animation_frame >= 90:
                return False
            elif combat_animation_frame > 30:
                try:
                    enemy.after_death(mainscreen)
                except:
                    return False

        pygame.display.update()

    if not combat_end:
        return None

def play():
    global mainscreen, text_box_original, mouse
    global player, rat, jacket
    
    
    mainscreen = pygame.display.set_mode((1600,900))
    pygame.display.set_caption("Circle of Violence")
    pygame.mouse.set_visible(False)

    
    text_box_original = pygame.image.load(os.path.join('assets', 'dialog box.png')).convert_alpha()
    player = player_class(100, 120)
    jacket = jacket_class()
    rat = rat_enemy()
    mouse = cursor()

    scene_play = scene1
    do_player_died = scene_play(True)
    while 1:
        
        if do_player_died == True:
            return True
        elif do_player_died == None:
            return None
        else:
            scene_play = do_player_died

        do_player_died = scene_play()


def main():
    pygame.init()
    quit_game = False
    while True:
        quit_game = play()
        if quit_game == None:
            break

    pygame.quit()

if __name__ == "__main__":
    main()