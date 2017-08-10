import block as b
import grid as g
import menu as m
import pygame


class TetrisApplication:
    def __init__(self, initial_state='menu'):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.time_start = 0
        self.time_stop = 60
        self.time_step = 1

        info_object = pygame.display.Info()
        self.window_width, self.window_height = info_object.current_w, info_object.current_h
        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)

        # self.window_width, self.window_height = 800, 600
        # self.window = pygame.display.set_mode((self.window_width, self.window_height))

        pygame.display.set_caption('Tetris')
        pygame.display.set_icon(pygame.image.load_extended('images/icon.gif'))
        pygame.mouse.set_visible(False)

        self.state_current = initial_state  # total states: 'menu', 'game', 'pause', 'game over'
        self.score = 0

        grid_dimensions = (10, 20)
        offset = (self.window_width // 2 - ((grid_dimensions[0] * int(self.window_height * (13 / 300))) // 2)), \
                 (self.window_height // 2 - ((grid_dimensions[1] * int(self.window_height * (13 / 300))) // 2))

        img_scale = int(self.window_height * (13 / 300))
        self.font_scale_x = int(self.window_width * (47 / 1366))
        self.font_scale_y = int(self.window_width * (16 / 768))

        self.stone = b.Stone(surface=self.window,
                             scale=img_scale,
                             offset=offset,
                             pos=(grid_dimensions[0] // 2, 0),
                             block_type='t',
                             rotation=0
                             )

        self.grid = g.Grid(surface=self.window,
                           scale=img_scale,
                           offset=offset,
                           grid_dimensions=grid_dimensions
                           )

        self.menu = m.Menu(surface=self.window,
                           window_dimensions=(self.window_width, self.window_height),
                           message_func=self.message
                           )

        pygame.mixer.music.load('audio/tetris_theme.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

        self.mainloop()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # the state_current determines what actions are available
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
                        if event.key == pygame.K_LEFT:
                            self.stone.move('left', self.grid)
                        if event.key == pygame.K_RIGHT:
                            self.stone.move('right', self.grid)
                        if event.key == pygame.K_DOWN:
                            self.stone.held = True
                        if event.key == pygame.K_RCTRL:
                            self.stone.drop(self.grid)
                        if event.key == pygame.K_UP:
                            self.stone.rotate('cw', self.grid)
                        if event.key == pygame.K_RETURN:
                            self.state_current = 'pause'
                        elif event.key == pygame.K_KP_ENTER:
                            self.state_current = 'pause'

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            self.stone.held = False

            elif self.state_current in 'pause':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state_current = 'game'
                    elif event.key == pygame.K_KP_ENTER:
                        self.state_current = 'game'
                    elif event.key == pygame.K_ESCAPE:
                        self.state_current = 'menu'

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
            pygame.display.update()
            self.clock.tick(self.time_stop)

    def state_menu(self):
        self.menu.render()
        if self.menu.play_status:
            self.state_current = 'game'

    def state_game(self):
        self.window.fill((0, 0, 0))
        self.grid.render_grid()
        self.stone.render_block()
        self.message(str(self.score), 3, (255, 255, 255), center='y', offset_arg=(2, 0))

        if self.stone.held:
            self.stone.move('down', self.grid, reset='enable')
            self.time_start = 0
        else:
            if self.time_tick():
                self.stone.move('down', self.grid, reset='enable')

        if self.stone.game_over(self.grid):
            self.state_current = 'game over'
            self.message('Game Over!', 3, (200, 200, 200), center='x', offset_arg=(0, 1))
            self.message('SPACE to reset', 2, (200, 200, 200), center='x', offset_arg=(0, 5))
            self.message('ESCAPE to go to menu', 2, (200, 200, 200), center='x', offset_arg=(0, 7))
            self.message('BACKSPACE to exit', 2, (200, 200, 200), center='x', offset_arg=(0, 9))

        while self.grid.line_clear():
            self.score += 1
            self.time_step += 0.2

    def state_pause(self):
        self.message("Paused!", 1, (255, 255, 255), center='xy')

    def time_tick(self):
        if self.time_start >= self.time_stop:
            self.time_start = 0
            return True
        else:
            self.time_start += int(self.time_step)

    def message(self, msg, font_size, font_color, pos=(0, 0), center='', offset_arg=(0, 0)):

        font = pygame.font.SysFont(None, font_size * self.font_scale_x)
        text_surface = font.render(msg, True, font_color)
        text_width, text_height = font.size(msg)

        offset = offset_arg[0] * self.font_scale_x * font_size, offset_arg[1] * self.font_scale_y * font_size
        placement = pos[0] + offset[0], pos[1] + offset[1]

        if center in 'x':
            placement = self.window_width // 2 - text_width // 2, pos[1] + offset[1]
        elif center in 'y':
            placement = pos[0] + offset[0], self.window_height // 2 - text_height // 2
        elif center in 'xy':
            placement = self.window_width // 2 - text_width // 2, self.window_height // 2 - text_height // 2

        self.window.blit(text_surface, placement)

if __name__ in '__main__':
    app = TetrisApplication()
