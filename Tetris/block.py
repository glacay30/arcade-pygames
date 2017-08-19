from random import randint
import pygame

img_red = pygame.image.load_extended('images/red.png')
img_orange = pygame.image.load_extended('images/orange.png')
img_yellow = pygame.image.load_extended('images/yellow.png')
img_green = pygame.image.load_extended('images/green.png')
img_blue = pygame.image.load_extended('images/blue.png')
img_teal = pygame.image.load_extended('images/teal.png')
img_pink = pygame.image.load_extended('images/pink.png')


class Block:
    def __init__(self, surface, scale, offset, pos, block_type, rotation):
        self.block_info = {
            't': (['08-888', '08-088-08', '-888-08', '08-88-08'], pygame.transform.scale(img_red, (scale, scale))),
            's': (['088-88', '8-88-08'], pygame.transform.scale(img_pink, (scale, scale))),
            'z': (['88-088', '08-88-8'], pygame.transform.scale(img_blue, (scale, scale))),
            'o': (['88-88'], pygame.transform.scale(img_yellow, (scale, scale))),
            'i': (['08-08-08-08', '8888'], pygame.transform.scale(img_teal, (scale, scale))),
            'j': (['08-08-88', '8-888', '088-08-08', '-888-008'], pygame.transform.scale(img_green, (scale, scale))),
            'l': (['08-08-088', '-888-8', '88-08-08', '008-888'], pygame.transform.scale(img_orange, (scale, scale))),
        }
        self.surface = surface
        self.pos = list(pos)
        self.standard_pos = pos
        self.block_type = block_type
        self.block_rotation = rotation
        self.offset = offset

        self.max_rotations = len(self.block_info[self.block_type][0])
        self.block_forms = self.block_info[self.block_type][0]
        self.block_image = self.block_info[self.block_type][1]

        self.scale = scale

        self.held = []
        self.held_count = 0
        self.held_end = 15
        self.truly_held = False
        self.first_time = True

    def render_block(self):
        cells = self.unpack(self.block_forms[self.block_rotation], self.pos)
        for cell in cells:
            self.surface.blit(self.block_image, (cell[0] * self.scale + self.offset[0],
                                                 cell[1] * self.scale + self.offset[1]))

    def game_over(self, grid):
        cells = self.unpack(self.block_forms[self.block_rotation], self.pos)
        for cell in cells:
            if grid.grid_data[tuple(cell)][0] == 1:
                return True
            else:
                continue
        return False

    @staticmethod
    def unpack(base, pos):
        """Takes the pattern '08-88' and returns [[x1, y1], [x2, y2],...]
        
            Keyword Arguments:
            base -- a string pattern; e.g. '888-808-888'
                8 means a block
                0 means a space
                - means a next line down
            pos -- grid coordinate of block
        """
        x, y, complete = 0, 0, []
        for char in base:
            if char in '0':
                x += 1
            elif char in '8':
                complete.append([pos[0] + x, pos[1] + y])
                x += 1
            elif char in '-':
                x = 0
                y += 1
        return complete


class Stone(Block):
    def move(self, direction, grid):
        change = {'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        blocked = False

        for cell in self.unpack(self.block_forms[self.block_rotation], self.pos):
            try:
                if grid.grid_data[(cell[0] + change[direction][0], cell[1] + change[direction][1])][0] == 1:
                    blocked = True
                    break
            except KeyError:
                blocked = True
                break

        if not blocked:
            self.pos = [self.pos[0] + change[direction][0], self.pos[1] + change[direction][1]]
        else:
            if 'down' in direction:
                self.new_block(grid)

    def count(self):
        self.held_count += 1
        if self.held_count >= self.held_end:
            self.held_count = 0
            return True
        return False

    def drop(self, grid):
        """Block moves down until it is blocked"""
        current_y = 0
        check_list = []
        while True:
            for cell in self.unpack(self.block_forms[self.block_rotation], self.pos):
                x, y = cell
                try:
                    if grid.grid_data[(x, y + 1 + current_y)][0] == 1:
                        check_list.append('blocked')
                except KeyError:
                    check_list.append('blocked')
            if 'blocked' in check_list:
                self.pos[1] += current_y
                self.new_block(grid)
                break
            else:
                current_y += 1

    def rotate(self, direction, grid):
        """Check if the direction of the rotation is clear and rotate if it is
            Keyword Arguments:
                direction -- either 'cw' or 'ccw', clockwise or counter-clockwise
                grid -- self.grid to reference from
        """
        new_rotation = None
        check_list = []
        if direction in 'cw' and self.block_rotation == self.max_rotations - 1:
            new_rotation = 0
        elif direction in 'cw':
            new_rotation = self.block_rotation + 1
        elif direction in 'ccw' and self.block_rotation == 0:
            new_rotation = self.max_rotations - 1
        elif direction in 'ccw':
            new_rotation = self.block_rotation - 1
        cells = self.unpack(self.block_forms[new_rotation], self.pos)
        for cell in cells:
            try:
                if grid.grid_data[tuple(cell)][0] == 1:
                    check_list.append('blocked')
            except KeyError:
                check_list.append('blocked')
        if 'blocked' not in check_list:
            self.block_rotation = new_rotation

    def new_block(self, grid):
        cells = self.unpack(self.block_forms[self.block_rotation], self.pos)
        grid.update_grid(cells, self.block_image)
        self.__init__(surface=self.surface,
                      scale=self.scale,
                      offset=self.offset,
                      pos=self.standard_pos,
                      block_type=['t', 's', 'z', 'o', 'i', 'j', 'l'][randint(0, 6)],
                      rotation=0,
                      )
