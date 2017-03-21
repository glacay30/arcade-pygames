import pygame
import assets as a


class TetrisApplication:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.width, self.height = 800, 600
        self.fps = 10
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Slither')
        self.game_state = ['menu', 'game']
        self.mainloop()

    def mainloop(self):
        while True:
            self.event_handling()
            if self.game_state[0] in 'menu':
                self.menu_loop()
            elif self.game_state[0] in 'game':
                self.game_loop()

    def game_loop(self):
        self.window.fill(a.grey)
        self.message(self.window, "Game window")
        self.Block.render_all(self.window)
        pygame.display.update()

    def menu_loop(self):
        self.window.fill(a.white)
        self.message(self.window, "Menu window")
        pygame.display.update()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_e:
                    self.game_state.reverse()

    class Block:
        def __init__(self, surface, pos, block_type, rotation=0):
            self.surface = surface
            self.block_type = block_type
            self.rotation = rotation
            self.pos = tuple(pos)
            self.size = 16
            self.block_list = {
                't': (['08-888', '8-88-8', '888-08', '08-88-08'], a.red_b),
                's': (['088-88', '8-88-08'], a.pink_b),
                'z': (['88-088', '08-88-8'], a.blue_b),
                'o': (['88-88'], a.yellow_b),
                'i': (['8-8-8-8', '8888'], a.teal_b),
                'j': (['08-08-88', '8-888', '88-8-8', '888-008'], a.green_b),
                'l': (['8-8-88', '888-8', '88-08-08', '008-888'], a.orange_b)
            }
            self.render_block()

        def render_block(self):
            base = self.block_list[self.block_type][0][self.rotation]
            color = self.block_list[self.block_type][1]
            unpacked = self.unpack(base, self.pos)
            for coords in unpacked:
                self.surface.blit(color, (coords[0] * self.size, coords[1] * self.size))

        @staticmethod
        def unpack(base, coordinate):
            x, y, complete = 0, 0, []
            for char in base:
                if char in '0':
                    x += 1
                elif char in '8':
                    complete.append([coordinate[0] + x, coordinate[1] + y])
                    x += 1
                elif char in '-':
                    x = 0
                    y += 1
            return complete

        @classmethod
        def render_all(cls, surface):
            b1 = cls(surface, [0, 3], 't', 0)
            b2 = cls(surface, [0, 8], 't', 1)
            b3 = cls(surface, [0, 13], 't', 2)
            b4 = cls(surface, [0, 18], 't', 3)
            b5 = cls(surface, [5, 3], 's', 0)
            b6 = cls(surface, [5, 8], 's', 1)
            b7 = cls(surface, [10, 3], 'z', 0)
            b8 = cls(surface, [10, 8], 'z', 1)
            b9 = cls(surface, [15, 3], 'o', 0)
            b10 = cls(surface, [20, 3], 'i', 0)
            b11 = cls(surface, [20, 8], 'i', 1)
            b12 = cls(surface, [25, 3], 'j', 0)
            b13 = cls(surface, [25, 8], 'j', 1)
            b14 = cls(surface, [25, 13], 'j', 2)
            b15 = cls(surface, [25, 18], 'j', 3)
            b16 = cls(surface, [30, 3], 'l', 0)
            b17 = cls(surface, [30, 8], 'l', 1)
            b18 = cls(surface, [30, 13], 'l', 2)
            b19 = cls(surface, [30, 18], 'l', 3)

    @staticmethod
    def message(surface, msg="Text", color=(0, 0, 0), size=40, pos=(0, 0)):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(msg, True, color)
        surface.blit(text_surface, pos)

if __name__ in '__main__':
    app = TetrisApplication()
