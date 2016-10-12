import pygame
pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

white = 255, 255, 255
black = 0, 0, 0

ball = pygame.image.load('C:/users/upsil_000/PycharmProjects/MyProject/src/ball.png')
ball_rect = ball.get_rect()
speed = [1, 1]
print(ball_rect.height)

while 1:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
            pygame.quit()
            break

    ball_rect = ball_rect.move(speed)
    if ball_rect.left < 0 or ball_rect.right > width:
        speed[0] = -speed[0]
    if ball_rect.top < 0 or ball_rect.bottom > height:
        speed[1] = -speed[1]
    screen.fill(black)
    screen.blit(ball, ball_rect)
    pygame.display.flip()
    pygame.time.delay(10)
