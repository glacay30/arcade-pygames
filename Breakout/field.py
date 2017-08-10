import pygame
from math import floor
from math import ceil

"""Grid is a dictionary
    (x, y): int
        where int is a value from 0 to n
        if 0, means no block
        if n, means yes block + color (color dependent on value)
"""

COLORS = (
    (23, 165, 51),
    (43, 43, 160),
    (163, 57, 57),
    (244, 164, 66),
)


class Field:
    def __init__(self, window):
        self.window = window
        self.field_width_percentage, self.field_height_percentage = 0.95, 0.3
        self.field_width, self.field_height = floor(window.get_width() * self.field_width_percentage), \
                                              floor(window.get_height() * self.field_height_percentage)

        self.grid_width, self.grid_height = 14, 8
        self.grid = dict(self.grid_setup(self.grid_width, self.grid_height))

        self.block_w = int(self.field_width * (1 / self.grid_width))
        self.block_h = int(self.field_height * (1 / self.grid_height))
        self.block_s = ceil(self.window.get_width() * (1 - self.field_width_percentage + 0.01) * (1 / self.grid_width))
        self.block_ws = int(self.block_w + self.block_s)
        self.block_hs = int(self.block_h + self.block_s)
        self.offset_y = int(self.field_height * 0.2)

    @staticmethod
    def grid_setup(w, h):
        for x in range(w):
            for y in range(h):
                n = 0 if y < 2 else 1 if y < 4 else 2 if y < 6 else 3 if y < 8 else 0
                yield (x, y), COLORS[n]

    def update(self, points):
        for point in points:
            x, y = point
            self.grid.pop((x // self.block_ws, (y - self.offset_y) // self.block_hs))
        if len(self.grid) == 0:
            return 'win'
        return ''

    def render(self):
        block = pygame.Surface((self.block_w, self.block_h))
        for k, v in self.grid.items():
            pos = self.block_ws * k[0], self.block_hs * k[1] + self.offset_y
            block.fill(v)
            self.window.blit(block, pos)
