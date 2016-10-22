import pygame

class Block:

    def __init__(self, surface, color, x, y, width, height):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
