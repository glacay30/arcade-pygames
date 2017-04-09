import assets as a
import block as b
import grid as g
import menu as m
import pygame


class TetrisApplication:
    def __init__(self, initial_state):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.time_start = 0
        self.time_stop = 60
        self.time_step = 1

        self.width, self.height = 240, 400
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Tetris')

        self.state_current = initial_state
        # total states: 'menu', 'game', 'pause', 'game over'
        self.score = 0
        self.offset = (2, 3)
        self.stone = b.Stone(self.window, (3, 0), [3, 0], self.offset, 't', 0)
        self.grid = g.Grid(self.window, (10, 20), self.offset)
        self.menu = m.Menu(self.window, self.message)
        pygame.mixer.music.load('audio/tetris_theme.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

        self.mainloop()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # this restricts the input based on what self.state_current currently is
            if self.state_current in 'menu':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.menu.activate()
                    if event.key == pygame.K_UP:
                        self.menu.highlight('up')
                    if event.key == pygame.K_DOWN:
                        self.menu.highlight('down')
                    if event.key == pygame.K_ESCAPE:
                        self.menu.back()

            elif self.state_current in 'game':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state_current = 'menu'
                            self.__init__('menu')
                        if event.key == pygame.K_a:
                            self.stone.move('left', self.grid)
                        if event.key == pygame.K_d:
                            self.stone.move('right', self.grid)
                        if event.key == pygame.K_s:
                            self.stone.move('down', self.grid)
                        if event.key == pygame.K_SPACE:
                            self.stone.drop(self.grid)
                        if event.key == pygame.K_LEFT:
                            self.stone.rotate('ccw', self.grid)
                        if event.key == pygame.K_RIGHT:
                            self.stone.rotate('cw', self.grid)
                        if event.key == pygame.K_t:
                            self.state_current = 'pause'

            elif self.state_current in 'pause':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.state_current = 'game'

            elif self.state_current in 'game over':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.__init__('game')
                    if event.key == pygame.K_ESCAPE:
                        self.__init__('menu')
                    if event.key == pygame.K_BACKSPACE:
                        pygame.quit()
                        quit()

    def mainloop(self):
        while True:
            self.event_handling()
            if self.state_current in 'menu':
                self.state_menu()
            elif self.state_current in 'game':
                pygame.mixer.music.unpause()
                self.state_game()
            elif self.state_current in 'pause':
                self.state_pause()
            elif self.state_current in 'game over':
                self.state_game_over()
            pygame.display.update()
            self.clock.tick(self.time_stop)

    def state_menu(self):
        self.menu.render()
        if self.menu.play_status:
            self.state_current = 'game'

    def state_game(self):
        self.window.fill(a.color_black)
        self.grid.render_grid()
        self.stone.render_block()
        self.message(str(self.score), pos=[5, self.height - 30])

        if self.time_tick():
            self.stone.move('down', self.grid, reset='enable')
        if self.stone.game_over(self.grid):
            self.state_current = 'game over'

        if self.grid.line_check():
            self.score += 1
            self.time_step += 0.2

    def state_pause(self):
        self.message("Paused!", center=(1, 1))

    def state_game_over(self):
        self.message('Game Over!', size=50, center=(1, 0), pos=(0, 20))
        self.message('SPACE to reset', size=30, center=(1, 0), pos=(0, 70))
        self.message('ESCAPE to go to menu', size=30, center=(1, 0), pos=(0, 100))
        self.message('BACKSPACE to exit', size=30, center=(1, 0), pos=(0, 130))

    def time_tick(self):
        if self.time_start >= self.time_stop:
            self.time_start = 0
            return True
        else:
            self.time_start += int(self.time_step)

    def message(self, msg, color=(255, 255, 255), size=40, pos=(0, 0), center=(0, 0)):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(msg, True, color)
        text_width, text_height = font.size(msg)

        if center[0] == 1 and center[1] == 1:
            self.window.blit(text_surface, (self.width // 2 - text_width // 2, self.height // 2 - text_height // 2))
        elif center[0] == 1:
            self.window.blit(text_surface, (self.width // 2 - text_width // 2, pos[1]))
        elif center[1] == 1:
            self.window.blit(text_surface, (pos[0], self.height // 2 - text_height // 2))
        else:
            self.window.blit(text_surface, pos)

if __name__ in '__main__':
    app = TetrisApplication('menu')
