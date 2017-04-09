import assets as a
from random import randint


class Block:
    def __init__(self, surface, standard_pos, pos, offset, block_type, rotation):
        self.block_info = {
            't': (['08-888', '08-088-08', '-888-08', '08-88-08'], a.img_red),
            's': (['088-88', '8-88-08'], a.img_pink),
            'z': (['88-088', '08-88-8'], a.img_blue),
            'o': (['88-88'], a.img_yellow),
            'i': (['8-8-8-8', '8888'], a.img_teal),
            'j': (['08-08-88', '8-888', '088-08-08', '-888-008'], a.img_green),
            'l': (['08-08-088', '-888-8', '88-08-08', '008-888'], a.img_orange)
        }
        self.surface = surface
        self.block_type = block_type
        self.block_rotation = rotation
        self.max_rotations = len(self.block_info[self.block_type][0])
        self.block_forms = self.block_info[self.block_type][0]
        self.block_color = self.block_info[self.block_type][1]
        self.offset = offset
        self.standard_pos = (standard_pos[0] + offset[0], standard_pos[1] + offset[1])
        self.pos = [pos[0] + offset[0], pos[1] + offset[1]]
        self.size = 16

    # def create_block(self, shape, pos, grid):
    #     cells = self.unpack(shape, pos)
    #     for cell in cells:
    #         grid.grid_data[tuple(cell)] = 1
    #         self.surface.blit(a.img_blank, (cell[0] * self.size, cell[1] * self.size))

    def render_block(self):
        base = self.block_forms[self.block_rotation]
        cells = self.unpack(base, tuple(self.pos))
        for cell in cells:
            self.surface.blit(self.block_color, (cell[0] * self.size, cell[1] * self.size))

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
        """Takes the pattern '08-88' and returns [[coord1],[coord2]...]
        
            Keyword Arguments:
            base -- a string pattern; e.g. '888-808-888'
                8 means a block
                0 means a space
                - means a next line down
            pos -- position to base rest of block creation on
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
    def move(self, direction, grid, reset='disable'):
        """Move block by one space unless something blocks it"""
        change = {'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        check_list = []
        for cell in self.unpack(self.block_forms[self.block_rotation], self.pos):
            x, y = cell
            try:
                if grid.grid_data[(x + change[direction][0], y + change[direction][1])][0] == 1:
                    check_list.append('blocked')
            except KeyError:
                check_list.append('blocked')
        if 'blocked' not in check_list:
            self.pos[0] += change[direction][0]
            self.pos[1] += change[direction][1]
        else:
            if 'enable' in reset:
                self.new_block(grid)

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
        grid.update_grid(cells, self.block_color)
        self.__init__(self.surface, self.standard_pos, list(self.standard_pos),
                      (0, 0), ['t', 's', 'z', 'o', 'i', 'j', 'l'][randint(0, 6)], 0)
