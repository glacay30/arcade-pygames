import pygame
from assests import *
from blocks import *

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Tetris')

fps = 60


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
        window.fill(black)
        alpha = Block(window, white, 100, 100, 50, 80)
        alpha.render()
        pygame.display.update()
        pygame.time.Clock().tick(fps)

    pygame.quit()
    quit()

game_menu()
