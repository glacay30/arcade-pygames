import pygame
from assets import *
from blocks import *

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Tetris')

fps = 60

alpha = Block('B_001', window, red, 50, 50, 60, 10)


def game_menu():
    menu = True
    color = 0

    while menu:
        for event in pygame.event.get():   # Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_f:
                    if color == 1:
                        color = 0
                    else:
                        color += 1
        window.fill(black)
        alpha.update()
        pygame.display.update()
        pygame.time.Clock().tick(fps)

    pygame.quit()
    quit()

game_menu()
