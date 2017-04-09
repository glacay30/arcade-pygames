import pygame
import assets as a


class Grid:
    def __init__(self, surface, grid_dimensions, offset):
        self.surface = surface
        self.grid_dimensions = grid_dimensions
        self.offset = offset
        self.grid_start = (self.offset[0], self.offset[1])
        self.grid_end = (self.grid_dimensions[0] + self.offset[0], self.grid_dimensions[1] + self.offset[1])
        self.grid_data = {(x, y): (0, a.img_grid)
                          for x in range(self.grid_start[0], self.grid_end[0])
                          for y in range(self.grid_start[1], self.grid_end[1])}

    def line_check(self):
        """Check if a line is made"""
        for y in range(self.grid_start[1], self.grid_end[1]):
            streak = 0
            for x in range(self.grid_start[0], self.grid_end[0]):
                if self.grid_data[(x, y)][0] == 1:
                    streak += 1
            if streak == self.grid_dimensions[0]:
                self.line_clear(y)
                return True
            else:
                continue
        return False

    def line_clear(self, row_to_clear):
        """Clear the line that was made"""
        y = row_to_clear
        for x in range(self.grid_start[0], self.grid_end[0]):
            self.grid_data[(x, y)] = (0, a.img_grid)
        self.line_clean(y)

    def line_clean(self, row_to_stop):
        """Move every block above the cleared line one below"""
        new_cells = {}

        for y in range(self.grid_start[1], row_to_stop):
            for x in range(self.grid_start[0], self.grid_end[0]):
                if self.grid_data[(x, y)][0] == 0:
                    new_cells[(x, y + 1)] = (0, a.img_grid)
                elif self.grid_data[(x, y)][0] == 1:
                    new_cells[(x, y + 1)] = (1, self.grid_data[(x, y)][1])
        for k, v in new_cells.items():
            self.grid_data[k] = v

    def update_grid(self, cells, color):
        for cell in cells:
            self.grid_data[tuple(cell)] = (1, color)

    def render_grid(self):
        for x in range(self.grid_start[0], self.grid_end[0]):
            for y in range(self.grid_start[1], self.grid_end[1]):
                self.surface.blit(self.grid_data[(x, y)][1], (x * 16, y * 16))
