import pygame

def draw_text(txt, font_size, padx, pady, surface, position, color=(0, 0, 0)):
    surface.fill((255, 255, 255))
    font = pygame.font.SysFont("monospace", font_size, True)
    space = font.size(' ')[0]
    text_array = [word.split(' ') for word in txt.splitlines()]
    width = surface.get_size()[0]
    x, y = position

    for j, line in enumerate(text_array):
        for i, word in enumerate(line):
            text = font.render(word, 1, color)
            text_w, text_h = text.get_size()
            if x + text_w >= width:
                x = position[0]
                y += text_h
            
            x += padx if i == 0 else 0
            y += pady if j == 0 else 0

            surface.blit(text,(x, y))
            x += text_w + space

        x = position[0]
        y += text_h