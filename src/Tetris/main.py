import pygame
from assets import *
from classes import *

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Tetris')

fps = 60

grid1 = PlayingField('grid1', 10, 22)
grid1.make_grid()
b_001 = Block('b_001', window, red, 50, 50, 60, 10)


def game_menu():
    menu = True

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
                    if b_001.image == 1:
                        b_001.image = 0
                    else:
                        b_001.image += 1
        window.fill(grey)
        b_001.render()
        pygame.display.update()
        pygame.time.Clock().tick(fps)

    pygame.quit()
    quit()

game_menu()
