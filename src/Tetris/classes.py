import pygame
from assets import *


class PlayingField:     # Creates the game-play grid
    def __init__(self, name, width, height):
        self.name = name
        print("Initialized: " + self.name)
        self.width = width
        self.height = height
        self.grid = {}

    def make_grid(self):    # makes grid by using a (x, y, z) coord, where z is 0 or 1 to show occupancy
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                cell_name = "cell{}".format(count)
                val = [j * 16, i * 16, 0]
                self.grid[cell_name] = val
                count += 1
        print('Grid created')
        return self.grid


class Block:    # Main block class that all types will inherit from
    def __init__(self, name, surface, color, x, y, width, height):
        self.name = name
        print("Initialized: " + self.name)
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.num_count = 0
        self.num_target = 20
        self.image = 0

    def render(self):  # basic render to show up on screen; checks for color to display
        if self.image == 0:
            pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        elif self.image == 1:
            pygame.draw.rect(self.surface, blue, (self.x, self.y, self.width, self.height))

    def update(self):  # basic animation that changes back and forth via num_target
        self.num_count += 1
        if self.num_count == self.num_target:
            if self.image == 1:
                self.image = 0
            elif self.image == 0:
                self.image = 1
            self.num_count = 0
        self.render()
