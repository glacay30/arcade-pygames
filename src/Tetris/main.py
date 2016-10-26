import pygame
import classes as c
import assets as a

pygame.init()

fps = 60
width, height = 800, 608
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris')

size = 16

grid1 = c.PlayingField('grid1', 10, 22)
grid1.make_grid()
test1 = c.TetraT('test1', window)
test2 = c.TetraO('test2', window)
test3 = c.TetraJ('test3', window)
test4 = c.TetraL('test4', window)
test5 = c.TetraS('test5', window)
test6 = c.TetraZ('test6', window)
test7 = c.TetraI('test7', window)


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
        window.fill(a.grey)
        i = 50
        test1.render(50, i)
        test2.render(150, i)
        test3.render(250, i)
        test4.render(350, i)
        test5.render(450, i)
        test6.render(550, i)
        test7.render(650, i)

        pygame.display.update()     # THIS GOES AFTER EVERYTHING HAS BEEN LOADED
        pygame.time.Clock().tick(fps)

    pygame.quit()
    quit()

game_menu()
