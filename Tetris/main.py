import assets as a
import block as b
import pygame


class TetrisApplication:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 10
        self.width, self.height = 800, 600
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Slither')
        self.state = 'menu'
        # total states: 'menu', 'game', 'pause'
        self.stone = b.Stone(self.window, [0, 1])

        self.mainloop()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # this restricts the input based on what self.state currently is
            if self.state in 'menu':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.state = 'game'
            elif self.state in 'game':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            self.state = 'menu'
                        if event.key == pygame.K_a:
                            self.stone.move_left()
                        if event.key == pygame.K_d:
                            self.stone.move_right()
                        if event.key == pygame.K_SPACE:
                            pass  # send down
                        if event.key == pygame.K_LEFT:
                            self.stone.rotate_ccw()
                        if event.key == pygame.K_RIGHT:
                            self.stone.rotate_cw()
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'pause'
            elif self.state in 'pause':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'game'

    def mainloop(self):
        while True:
            self.event_handling()
            if self.state in 'menu':
                self.state_menu()
            elif self.state in 'game':
                self.state_game()
            elif self.state in 'pause':
                self.state_pause()
            pygame.display.update()
            self.clock.tick(self.fps)

    def state_menu(self):
        self.window.fill(a.color_white)
        self.message(self.window, "Menu window")

    def state_game(self):
        self.window.fill(a.color_grey)
        self.message(self.window, "Game window")
        # b.Block.render_all(self.window)
        if self.stone.time_tick():
            self.stone.move_down()
        self.stone.render_block()

    def state_pause(self):
        self.message(self.window, "Pause window", pos=(int(self.width / 2), int(self.height / 2)))

    @staticmethod
    def message(surface, msg="Text", color=(0, 0, 0), size=40, pos=(0, 0)):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(msg, True, color)
        surface.blit(text_surface, pos)

if __name__ in '__main__':
    app = TetrisApplication()
