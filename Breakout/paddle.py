import pygame
from math import ceil

WHITE = (255, 255, 255)


class Paddle:
    def __init__(self, window):
        self.window = window
        self.surface = pygame.Surface((ceil(window.get_width() * 0.1), ceil(window.get_height() * 0.013)))
        self.surface.fill(WHITE)
        self.w = self.surface.get_width()
        self.h = self.surface.get_height()
        self.pos = [pygame.mouse.get_pos()[0], int(window.get_height() * 0.8)]
        self.pos_offset = 10
        self.col = {}
        self.set_col()

    def render_col(self):
        i = pygame.Surface([1, 1])
        i.fill((0, 200, 0))
        for point in self.col.keys():
            self.window.blit(i, point)

    def mouse(self, point):
        self.pos[0] = point[0]
        if self.pos[0] >= self.window.get_width() - self.w:
            self.pos[0] = self.window.get_width() - self.w
            pygame.mouse.set_pos(self.pos)
        self.set_col()

    def set_col(self):
        self.col = {}
        for x in range(self.pos[0], self.pos[0] + self.w // 2):
            self.col[(x, self.pos[1])] = 'left'
        for x in range(self.pos[0] + (self.w // 2), self.pos[0] + self.w):
            self.col[(x, self.pos[1])] = 'right'
