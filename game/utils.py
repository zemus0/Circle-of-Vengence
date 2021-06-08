import pygame

def draw_text(txt, font_size, padx, pady, width, screen, position, color=(0, 0, 0)):
    font = pygame.font.SysFont("monospace", font_size, True)
    space = font.size(' ')[0]
    text_array = [word.split(' ') for word in txt.splitlines()]
    x, y = position

    for line in text_array:
        for word in line:
            text = font.render(word, 1, color)
            text_w, text_h = text.get_size()
            if x + text_w >= width:
                x = position[0]
                y += text_h
            
            x += padx if x == 0 else 0
            y += pady if y == 0 else 0

            screen.blit(text,(x, y))
            x += text_w + space

        x = position[0]
        y += text_h
