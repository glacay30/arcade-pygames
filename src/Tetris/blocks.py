import pygame
from assets import *


class Block:
    def __init__(self, name, surface, color, x, y, width, height):
        self.name = name
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.num_count = 0
        self.num_target = 7
        self.image = 0
        print("Initilized: " + self.name)

    def update(self):
        self.num_count += 1
        if self.num_count == self.num_target:
            if self.image == 1:
                self.image = 0
            elif self.image == 0:
                self.image = 1
            self.num_count = 0
        if self.image == 0:
            pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        elif self.image == 1:
            pygame.draw.rect(self.surface, blue, (self.x, self.y, self.width, self.height))
