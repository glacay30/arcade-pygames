import pygame
import random

pygame.init()
disp_width = 256
disp_height = 256

clock = pygame.time.Clock()
fps = 10

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 155)

direction = 0
north = 90
east = 0
south = 270
west = 180

with open('best_score', 'r') as f1:
    best_score = int(f1.read())

game_display = pygame.display.set_mode((disp_width, disp_height))
pygame.display.set_caption('Slither')

font_size = 23
font = pygame.font.SysFont(None, font_size)

head_img = pygame.image.load('images/snake_head.png')
body_img = pygame.image.load('images/snake_body.png')
tail_img = pygame.image.load('images/snake_tail.png')
apple_img = pygame.image.load('images/apple.png')


def snake(coords_list):
    head = pygame.transform.rotate(head_img, direction)
    game_display.blit(head, (coords_list[-1][0], coords_list[-1][1]))

    for pos in coords_list[:-1]:
        body = pygame.transform.rotate(body_img, direction)
        game_display.blit(body, (pos[0], pos[1]))


def text_objects(text, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace=0):
    text_surf, text_rect = text_objects(msg, color)
    text_rect.center = (disp_width / 2), (disp_height / 2 + y_displace)
    game_display.blit(text_surf, text_rect)


def score_counter(c_score, b_score):
    text_surf_c = font.render(str(c_score), True, blue)
    text_surf_b = font.render(str(b_score), True, blue)
    game_display.blit(text_surf_c, [1, 1])
    game_display.blit(text_surf_b, [disp_width - text_surf_b.get_width() - 1, 1])


def pause():
    pause_game = True
    message_to_screen("Paused!", black)
    pygame.display.update()

    while pause_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game is quit by QUIT in game_intro")
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    print("Game is quit by ESCAPE/Q in game_intro")
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    pause_game = False


def game_intro():
    global best_score
    intro = True
    erase = False

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game is quit by QUIT in game_intro")
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    print("Game is quit by ESCAPE/Q in game_intro")
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    intro = False
                    print("Intro end by C")
                if event.key == pygame.K_f:
                    erase = True

        game_display.fill(white)
        message_to_screen("Start Menu", blue, -20)
        message_to_screen("Press C to Start", blue)

        if not erase:
            message_to_screen("Press F to reset best score of {}".format(str(best_score)), blue, 20)
        else:
            message_to_screen("Erased!", blue, 20)
            with open('best_score', 'w') as f:
                f.write('0')
            best_score = 0
        pygame.display.update()


def game_loop():
    global direction, best_score
    game_exit = False
    game_over = False

    speed = 16
    apple_size = 16
    lead_x = disp_width / 2
    lead_y = disp_height / 2
    lead_x_change = 0
    lead_y_change = 0

    current_score = 0

    snake_coords = []
    snake_directions = []
    snake_length = 1

    rand_apple_x = disp_width / 2 + 96
    rand_apple_y = disp_height / 2

    while not game_exit:
        game_display.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_exit = True
                if event.key == pygame.K_q:
                    game_exit = True
                if event.key == pygame.K_SPACE:
                    pause()

                # Color changer
                # if event.key == pygame.K_1:
                #     block_color = red
                # elif event.key == pygame.K_2:
                #     block_color = green
                # elif event.key == pygame.K_3:
                #     block_color = blue
                # elif event.key == pygame.K_4:
                #     block_color = black

                # Snake Movement - WASD
                if event.key == pygame.K_a:
                    if lead_x_change == speed:
                        continue
                    else:
                        lead_x_change = -speed
                        lead_y_change = 0
                        direction = west
                        print("Left by A")
                        break
                elif event.key == pygame.K_d:
                    if lead_x_change == -speed:
                        continue
                    else:
                        lead_x_change = speed
                        lead_y_change = 0
                        direction = east
                        print("Right by D")
                        break
                elif event.key == pygame.K_w:
                    if lead_y_change == speed:
                        continue
                    else:
                        lead_y_change = -speed
                        lead_x_change = 0
                        direction = north
                        print("Up by W")
                        break
                elif event.key == pygame.K_s:
                    if lead_y_change == -speed:
                        continue
                    else:
                        lead_y_change = speed
                        lead_x_change = 0
                        direction = south
                        print("Down by S")
                        break

                # Snake Movement - Arrow Keys
                if event.key == pygame.K_LEFT:
                    if lead_x_change == speed:
                        continue
                    else:
                        lead_x_change = -speed
                        lead_y_change = 0
                        direction = west
                        print("LEFT")
                        break
                elif event.key == pygame.K_RIGHT:
                    if lead_x_change == -speed:
                        continue
                    else:
                        lead_x_change = speed
                        lead_y_change = 0
                        direction = east
                        print("RIGHT")
                        break
                elif event.key == pygame.K_UP:
                    if lead_y_change == speed:
                        continue
                    else:
                        lead_y_change = -speed
                        lead_x_change = 0
                        direction = north
                        print("UP")
                        break
                elif event.key == pygame.K_DOWN:
                    if lead_y_change == -speed:
                        continue
                    else:
                        lead_y_change = speed
                        lead_x_change = 0
                        direction = south
                        print("DOWN")
                        break

        lead_x += lead_x_change
        lead_y += lead_y_change

        snake_head_pos = [lead_x, lead_y]
        snake_coords.append(snake_head_pos)
        snake_directions.append(direction)

        if snake_length > 1:
            tail = pygame.transform.rotate(tail_img, snake_directions[1])
            game_display.blit(tail, (snake_coords[0][0], snake_coords[0][1]))

        if len(snake_coords) > snake_length:
            del snake_coords[0]
            snake_directions.remove(snake_directions[0])

        if snake_head_pos in snake_coords[:-1]:
            game_over = True
            print("Death by self-collision")

        for pos in snake_coords:
            if pos[0] == rand_apple_x and pos[1] == rand_apple_y:
                rand_apple_x = random.randrange(0, disp_width - apple_size, 16)
                rand_apple_y = random.randrange(0, disp_height - apple_size, 16)
                snake_length += 1
                current_score += 1
                print("*")

        if current_score > best_score:
            best_score = current_score

        game_display.blit(apple_img, [rand_apple_x, rand_apple_y])
        snake(snake_coords)
        score_counter(current_score, best_score)

        if (lead_x >= disp_width) or \
                (lead_x <= -16) or \
                (lead_y >= disp_height) or \
                (lead_y <= -16):
            game_over = True
            print("Death by border collision")

        pygame.display.update()
        clock.tick(fps)

        while game_over:
            game_display.fill(white)
            message_to_screen("You died", red)
            message_to_screen("C to play again, Q to quit", black, font_size)
            score_counter(current_score, best_score)
            pygame.display.update()

            with open('best_score', 'w') as f2:
                f2.write(str(best_score))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    game_exit = True
                    print("Game is quit by QUIT in game_over")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_loop()
                        print("Game is replayed by C in game_over")
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        game_over = False
                        game_exit = True
                        print("Game is quit by ESCAPE/Q in game_over")

    pygame.quit()
    quit()

game_intro()
game_loop()
