import pygame
from random import randint
import field
import paddle
import ball
import menu

FPS = 60

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0


class BreakoutApp:
    def __init__(self, state='menu'):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        self.clock = pygame.time.Clock()

        self.window_width, self.window_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)

        # self.window_width, self.window_height = 640, 400
        # self.window = pygame.display.set_mode((self.window_width, self.window_height))

        self.paddle = paddle.Paddle(window=self.window)
        self.ball = ball.Ball(window=self.window)
        self.field = field.Field(window=self.window)
        self.menu = menu.Menu(window=self.window)

        self.sounds = {
            'win': pygame.mixer.Sound('sounds/win.ogg'),
            'lose': pygame.mixer.Sound('sounds/lose.ogg'),
            'hit1': pygame.mixer.Sound('sounds/hit1.ogg'),
            'hit2': pygame.mixer.Sound('sounds/hit2.ogg'),
            'hit3': pygame.mixer.Sound('sounds/hit3.ogg'),
        }

        self.score_num = 0
        self.score_size = int(self.window.get_height() * 0.2)
        self.score_surf = pygame.font.SysFont(None, self.score_size).render(str(self.score_num), True, WHITE)

        self.state = state

        self.main()

    def main(self):
        while True:
            self.event_handler()
            if self.state == 'game':
                self.game_loop()
            elif self.state == 'menu':
                self.menu.loop()
            pygame.display.flip()
            self.clock.tick(FPS)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.MOUSEMOTION:
                self.paddle.mouse(pygame.mouse.get_pos())

            if self.state in 'menu':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        if self.menu.button_check(pygame.mouse.get_pos()):
                            self.state = 'game'
                if event.type == pygame.MOUSEMOTION:
                    self.menu.button_highlight(pygame.mouse.get_pos())

            elif self.state in 'lose':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        BreakoutApp(state='game')
                    elif event.button == 3:  # right click
                        BreakoutApp(state='menu')

    def game_loop(self):
        pygame.event.set_grab(1)  # restrict mouse to window
        pygame.mouse.set_visible(False)
        self.window.fill(BLACK)
        # self.ball.render_path()
        self.window.blit(self.paddle.surface, self.paddle.pos)
        self.window.blit(self.ball.surface, self.ball.pos)
        self.field.render()
        self.window.blit(self.score_surf,
                         [int(self.window.get_width() * 0.02),
                          self.window.get_height() - self.score_surf.get_height()])
        # self.paddle.render_col()
        # self.ball.render_col()

        # Display FPS to screen
        # font = pygame.font.SysFont(None, 25).render(str(int(self.clock.get_fps())) + " FPS", True, WHITE)
        # self.window.blit(font, [0, 0])

        # Automatically move paddle
        # self.paddle.pos[0] = self.ball.pos[0] - (self.paddle.surface.get_width() // 2) + self.paddle.pos_offset
        # self.paddle.set_col()

        result, points = self.ball.collision(self.field, self.paddle)
        if 'field' in result:
            self.sounds['hit' + str(randint(1, 3))].play()
            self.score_num += len(points)
            self.score_surf = pygame.font.SysFont(None, self.score_size).render(str(self.score_num), True, WHITE)
            if 'win' in self.field.update(points):
                # reset the field and ball to keep playing
                self.sounds['win'].play()
                self.field = field.Field(window=self.window)
                self.ball = ball.Ball(window=self.window)
        elif 'paddle' in result:
            self.sounds['hit' + str(randint(1, 3))].play()
            self.paddle.pos_offset = 15 if randint(0, 1) else -15
        elif 'lose' in result:
            self.sounds['lose'].play()
            size = int(self.window_width * 0.078) + 1
            base = pygame.font.SysFont(None, size)
            m1 = base.render("You Lost!", True, WHITE)
            m2 = base.render("Left-click to play again", True, WHITE)
            m3 = base.render("Right-click to return to menu", True, WHITE)

            w4 = m3.get_width()
            h1, h2, h3 = m1.get_height(), m2.get_height(), m3.get_height()

            panel = pygame.Surface((w4, h1 + h2 + h3))
            panel.fill((100, 100, 100))
            panel.blit(m1, (0, 0))
            panel.blit(m2, (0, h1))
            panel.blit(m3, (0, h1 + h2))
            self.window.blit(panel, (self.window.get_width() // 2 - panel.get_width() // 2,
                                     self.window.get_height() // 2 - panel.get_height() // 2))
            self.state = 'lose'
            pygame.event.set_grab(0)

        self.ball.pos[0] += self.ball.direction[0] * self.ball.change
        self.ball.pos[1] += self.ball.direction[1] * self.ball.change
        self.ball.update_path()

if __name__ in '__main__':
    app = BreakoutApp()
