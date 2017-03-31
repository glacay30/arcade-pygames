import assets as a


class Block:
    def __init__(self, surface, pos, block_type='t', rotation=0):
        self.surface = surface
        self.block_type = block_type
        self.block_rotation = rotation
        self.pos = pos
        self.size = 16
        self.block_info = {
            't': (['08-888', '08-088-08', '-888-08', '08-88-08'], a.img_red),
            's': (['088-88', '8-88-08'], a.img_pink),
            'z': (['88-088', '08-88-8'], a.img_blue),
            'o': (['88-88'], a.img_yellow),
            'i': (['8-8-8-8', '8888'], a.img_teal),
            'j': (['08-08-88', '8-888', '088-08-08', '-888-008'], a.img_green),
            'l': (['08-08-088', '-888-8', '88-08-08', '008-888'], a.img_orange)
        }
        self.time_start = 0
        self.time_stop = 10
        self.time_step = 1

    def time_tick(self):
        if self.time_start == self.time_stop:
            self.time_start = 0
            return True
        else:
            self.time_start += self.time_step

    def render_block(self):
        base = self.block_info[self.block_type][0][self.block_rotation]
        color = self.block_info[self.block_type][1]
        unpacked = self.unpack(base, tuple(self.pos))
        for coords in unpacked:
            self.surface.blit(color, (coords[0] * self.size, coords[1] * self.size))

    # takes the pattern '08-88' and returns [[coord1],[coord2]...]
    @staticmethod
    def unpack(base, coordinate):
        x, y, complete = 0, 0, []
        for char in base:
            if char in '0':
                x += 1
            elif char in '8':
                complete.append([coordinate[0] + x, coordinate[1] + y])
                x += 1
            elif char in '-':
                x = 0
                y += 1
        return complete

    # call this and render every possible block on the screen
    @classmethod
    def render_all(cls, surface):
        b1 = cls(surface, [0, 3], 't', 0)
        b2 = cls(surface, [0, 8], 't', 1)
        b3 = cls(surface, [0, 13], 't', 2)
        b4 = cls(surface, [0, 18], 't', 3)
        b5 = cls(surface, [5, 3], 's', 0)
        b6 = cls(surface, [5, 8], 's', 1)
        b7 = cls(surface, [10, 3], 'z', 0)
        b8 = cls(surface, [10, 8], 'z', 1)
        b9 = cls(surface, [15, 3], 'o', 0)
        b10 = cls(surface, [20, 3], 'i', 0)
        b11 = cls(surface, [20, 8], 'i', 1)
        b12 = cls(surface, [25, 3], 'j', 0)
        b13 = cls(surface, [25, 8], 'j', 1)
        b14 = cls(surface, [25, 13], 'j', 2)
        b15 = cls(surface, [25, 18], 'j', 3)
        b16 = cls(surface, [30, 3], 'l', 0)
        b17 = cls(surface, [30, 8], 'l', 1)
        b18 = cls(surface, [30, 13], 'l', 2)
        b19 = cls(surface, [30, 18], 'l', 3)
        for block in ['b{}'.format(i) for i in range(1, 20)]:
            locals()[block].render_block()


class Stone(Block):
    def move_right(self):
        self.pos[0] += 1

    def move_left(self):
        self.pos[0] -= 1

    def move_down(self):
        self.pos[1] += 1

    def rotate_ccw(self):
        # cycle through the rotations in the left direction [0 <- n]
        if self.block_rotation == 0:
            self.block_rotation = len(self.block_info[self.block_type][0]) - 1
        else:
            self.block_rotation -= 1

    def rotate_cw(self):
        # cycle through the rotations in the right direction [0 -> n]
        if self.block_rotation == len(self.block_info[self.block_type][0]) - 1:
            self.block_rotation = 0
        else:
            self.block_rotation += 1
