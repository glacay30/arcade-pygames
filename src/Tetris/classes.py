import assets as a


class PlayingField(object):  # Creates the game-play grid
    def __init__(self, name, width, height):
        self.name = name
        print("Initialized: " + self.name)
        self.width = width
        self.height = height
        self.grid = {}

    def make_grid(self):  # Makes grid by using a (x, y, z) coord, where z is 0 or 1 to show occupancy
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                cell_name = "cell{}".format(count)
                val = [j * 16, i * 16, 0]
                self.grid[cell_name] = val
                count += 1
        print('Grid created')
        return self.grid


class Block(object):  # Main block class that all types inherit
    def __init__(self, name, surface):
        self.name = name
        print("Initialized: " + self.name)
        self.surface = surface


class TetraT(Block):
    def __init__(self, name, surface):      # 0|1|0
        super().__init__(name, surface)     # 1|1|1
        self.image = a.red_b

    def render(self, x, y):
        self.surface.blit(self.image, (x, y - 16))  # top-middle
        self.surface.blit(self.image, (x - 16, y))  # bottom-left
        self.surface.blit(self.image, (x, y))       # bottom-middle ---- (this indicates center of block)
        self.surface.blit(self.image, (x + 16, y))  # bottom-right


class TetraO(Block):
    def __init__(self, name, surface):      # 1|1
        super().__init__(name, surface)     # 1|1
        self.image = a.yellow_b

    def render(self, x, y):
        self.surface.blit(self.image, (x - 16, y - 16))     # top-left
        self.surface.blit(self.image, (x, y - 16))          # top-right
        self.surface.blit(self.image, (x - 16, y))          # bottom-left
        self.surface.blit(self.image, (x, y))               # bottom-right ----


class TetraJ(Block):
    def __init__(self, name, surface):      # 1|0|0
        super().__init__(name, surface)     # 1|1|1
        self.image = a.green_b

    def render(self, x, y):
        self.surface.blit(self.image, (x - 16, y - 16))     # top-left
        self.surface.blit(self.image, (x - 16, y))          # bottom-left
        self.surface.blit(self.image, (x, y))               # bottom-middle ----
        self.surface.blit(self.image, (x + 16, y))          # bottom-right


class TetraL(Block):
    def __init__(self, name, surface):      # 0|0|1
        super().__init__(name, surface)     # 1|1|1
        self.image = a.orange_b

    def render(self, x, y):
        self.surface.blit(self.image, (x + 16, y - 16))     # top-right
        self.surface.blit(self.image, (x - 16, y))          # bottom-left
        self.surface.blit(self.image, (x, y))               # bottom-middle ----
        self.surface.blit(self.image, (x + 16, y))          # bottom-right


class TetraS(Block):
    def __init__(self, name, surface):      # 0|1|1
        super().__init__(name, surface)     # 1|1|0
        self.image = a.pink_b

    def render(self, x, y):
        self.surface.blit(self.image, (x, y - 16))          # top-middle
        self.surface.blit(self.image, (x + 16, y - 16))     # top-right
        self.surface.blit(self.image, (x - 16, y))          # bottom-left
        self.surface.blit(self.image, (x, y))               # bottom-middle ----


class TetraZ(Block):
    def __init__(self, name, surface):      # 1|1|0
        super().__init__(name, surface)     # 0|1|1
        self.image = a.blue_b

    def render(self, x, y):
        self.surface.blit(self.image, (x - 16, y - 16))     # top-left
        self.surface.blit(self.image, (x, y - 16))          # top-middle
        self.surface.blit(self.image, (x, y))               # bottom-middle ----
        self.surface.blit(self.image, (x + 16, y))          # bottom-right


class TetraI(Block):
    def __init__(self, name, surface):      # 1|1|1|1
        super().__init__(name, surface)
        self.image = a.teal_b

    def render(self, x, y):
        self.surface.blit(self.image, (x - 32, y))      # left
        self.surface.blit(self.image, (x - 16, y))      # left-middle
        self.surface.blit(self.image, (x, y))           # right-middle ----
        self.surface.blit(self.image, (x + 16, y))      # right
