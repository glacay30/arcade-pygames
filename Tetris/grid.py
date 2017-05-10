import pygame

img_grid = pygame.image.load_extended('images/grid.png')


class Grid:
    def __init__(self, surface, scale, offset, grid_dimensions):
        self.surface = surface
        self.grid_w, self.grid_h = (grid_dimensions[0], grid_dimensions[1])
        self.offset = offset
        self.scale = scale
        self.img_grid = pygame.transform.scale(img_grid, (scale, scale))

        self.grid_data = {(x, y): (0, self.img_grid)
                          for x in range(self.grid_w)
                          for y in range(self.grid_h)}

    def line_check(self):
        """Check if a line is made"""
        for y in range(self.grid_h - 1, -1, -1):  # start from the bottom row to the top
            streak = 0
            for x in range(self.grid_w):
                if self.grid_data[(x, y)][0] == 1:
                    streak += 1
            if streak == self.grid_w:
                self.line_clear(y)
                self.line_clean(y)
                return True
            else:
                continue
        return False

    def line_clear(self, row_to_clear):
        """Clear the line that was made"""
        y = row_to_clear
        for x in range(self.grid_w):
            self.grid_data[(x, y)] = (0, self.img_grid)

    def line_clean(self, row_to_stop):
        """Move every block above the cleared line one below"""
        new_cells = {}

        for y in range(row_to_stop):
            for x in range(self.grid_w):
                new_cells[(x, y + 1)] = self.grid_data[(x, y)]
        for k, v in new_cells.items():
            self.grid_data[k] = v

    def update_grid(self, cells, color):
        for cell in cells:
            self.grid_data[tuple(cell)] = (1, color)

    def render_grid(self):
        for x in range(self.grid_w):
            for y in range(self.grid_h):
                self.surface.blit(self.grid_data[(x, y)][1],
                                  (x * self.scale + self.offset[0], y * self.scale + self.offset[1]))
