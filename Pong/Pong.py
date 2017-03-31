import pygame

pygame.init()
width, height = 256, 256

clock = pygame.time.Clock()
fps = 60

white = (255, 255, 255)
grey = (128, 128, 128)
black = (0, 0, 0)

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

f_size = 30
font = pygame.font.SysFont(None, f_size)

paddle_img = pygame.image.load('paddle.png')
paddle_rect_LEFT = paddle_img.get_rect().move([25, int(height / 2)])
paddle_rect_RIGHT = paddle_img.get_rect().move([width - 26, int(height / 2)])
ball_img = pygame.image.load('ball.png')
ball_rect = ball_img.get_rect().move([int(width / 2) - 70, int(height / 2) + 10])


def text_objects(text, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace=0):
    text_surf, text_rect = text_objects(msg, color)
    text_rect.center = (width / 2), (height / 2 + y_displace)
    display.blit(text_surf, text_rect)


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    intro = False

        message_to_screen('Start Screen', white, -30)
        message_to_screen('W/S to control left paddle', white)
        message_to_screen('I/K to control right paddle', white, 30)
        message_to_screen('Space to start', white, 60)
        pygame.display.update()


def score_counter(l_score, r_score):
    text_surf_l = font.render(str(l_score), True, white)
    text_surf_r = font.render(str(r_score), True, white)
    display.blit(text_surf_l, [1, 1])
    display.blit(text_surf_r, [width - text_surf_r.get_width() - 1, 1])


def game_loop():
    global ball_rect, paddle_rect_LEFT, paddle_rect_RIGHT

    play = True
    paddle_speed = 4
    direction_left = 'still'
    direction_right = 'still'
    ball_speed = [2, 1]
    score_left, score_right = 0, 0

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play = False
                if event.key == pygame.K_w:
                    direction_left = 'up'
                elif event.key == pygame.K_s:
                    direction_left = 'down'
                if event.key == pygame.K_i:
                    direction_right = 'up'
                elif event.key == pygame.K_k:
                    direction_right = 'down'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    direction_left = 'still'
                if event.key == pygame.K_i or event.key == pygame.K_k:
                    direction_right = 'still'

        ball_rect = ball_rect.move(ball_speed)

        if ball_rect.top < 0 or ball_rect.bottom > height:
            ball_speed[1] = -ball_speed[1]
        elif ball_rect.left <= 0:
            score_right += 1
            ball_rect = ball_img.get_rect().move([int(width / 2), int(height / 2) + 10])
            ball_speed[0] = -ball_speed[0]
        elif ball_rect.right >= width:
            score_left += 1
            ball_rect = ball_img.get_rect().move([int(width / 2), int(height / 2) + 10])
            ball_speed[0] = -ball_speed[0]

        if paddle_rect_LEFT.top <= 0:
            paddle_rect_LEFT.top = 0
        elif paddle_rect_LEFT.bottom >= height:
            paddle_rect_LEFT.bottom = height

        if paddle_rect_RIGHT.top <= 0:
            paddle_rect_RIGHT.top = 0
        elif paddle_rect_RIGHT.bottom >= height:
            paddle_rect_RIGHT.bottom = height

        if ball_rect.left == paddle_rect_LEFT.right - 1:
            for i in range(paddle_rect_LEFT.top, paddle_rect_LEFT.bottom):
                for j in range(ball_rect.top, ball_rect.bottom):
                    if j == i:
                        ball_speed[0] = -ball_speed[0]
                        break
                if j == i:
                    break
        elif ball_rect.right == paddle_rect_RIGHT.left + 1:
            for k in range(paddle_rect_RIGHT.top, paddle_rect_RIGHT.bottom):
                for l in range(ball_rect.top, ball_rect.bottom):
                    if k == l:
                        ball_speed[0] = -ball_speed[0]
                        break
                if k == l:
                    break

        if direction_left in 'up':
            paddle_rect_LEFT = paddle_rect_LEFT.move([0, -paddle_speed])
        elif direction_left in 'down':
            paddle_rect_LEFT = paddle_rect_LEFT.move([0, paddle_speed])
        elif direction_left in 'still':
            paddle_rect_LEFT = paddle_rect_LEFT.move([0, 0])

        if direction_right in 'up':
            paddle_rect_RIGHT = paddle_rect_RIGHT.move([0, -paddle_speed])
        elif direction_right in 'down':
            paddle_rect_RIGHT = paddle_rect_RIGHT.move([0, paddle_speed])
        elif direction_right in 'still':
            paddle_rect_RIGHT = paddle_rect_RIGHT.move([0, 0])

        display.fill(black)
        display.blit(ball_img, ball_rect)
        display.blit(paddle_img, paddle_rect_LEFT)
        display.blit(paddle_img, paddle_rect_RIGHT)
        score_counter(score_left, score_right)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

game_intro()
game_loop()
