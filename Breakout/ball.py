import pygame

WHITE = (255, 255, 255)


class Ball:
    def __init__(self, window):
        self.window = window
        self.window_w = window.get_width()
        self.window_h = window.get_height()

        self.radius = int(self.window_h * 0.01)
        self.surface = pygame.Surface([self.radius * 2, self.radius * 2])
        pygame.draw.circle(self.surface, WHITE, (self.radius, self.radius), self.radius)

        self.pos = [self.window_w // 2, int(self.window_h * 0.7)]
        self.pos_history = {}
        self.change = int(self.radius - 1)
        self.direction = [1, -1]

    def update_path(self):
        if tuple(self.pos) in self.pos_history:
            self.pos_history[tuple(self.pos)] += 1
        else:
            self.pos_history[tuple(self.pos)] = 1

    def render_path(self):
        surf = pygame.Surface((self.radius, self.radius))
        # surf.fill((150, 0, 0))
        for pos, count in self.pos_history.items():
            color = count * 20
            color = 255 if color >= 255 else color
            surf.fill((color, color, color))
            self.window.blit(surf, [pos[0] + self.radius // 4, pos[1] + self.radius // 4])

    def render_col(self):
        surf = pygame.Surface((1, 1))
        surf.fill((255, 0, 0))

        all_points = {}
        left, right, top, bottom = \
            self.pos[0], \
            self.pos[0] + self.surface.get_width(), \
            self.pos[1], \
            self.pos[1] + self.surface.get_height()
        quarter_w, quarter_h = self.surface.get_width() // 4, self.surface.get_height() // 4
        if self.direction == [-1, -1]:
            # left, top
            all_points['vertical'] = [[left, y] for y in range(top + 1, bottom - quarter_h)]
            all_points['horizontal'] = [[x, top] for x in range(left + 1, right - quarter_w)]
        elif self.direction == [1, -1]:
            # right, top
            all_points['vertical'] = [[right, y] for y in range(top + 1, bottom - quarter_h)]
            all_points['horizontal'] = [[x, top] for x in range(left + quarter_w, right)]
        elif self.direction == [1, 1]:
            # right, bot
            all_points['vertical'] = [[right, y] for y in range(top + quarter_h, bottom)]
            all_points['horizontal'] = [[x, bottom] for x in range(left + quarter_w, right)]
        elif self.direction == [-1, 1]:
            # left, bot
            all_points['vertical'] = [[left, y] for y in range(top + quarter_h, bottom)]
            all_points['horizontal'] = [[x, bottom] for x in range(left + 1, right - quarter_w)]

        for points in all_points.values():
            for point in points:
                self.window.blit(surf, point)

    def collision(self, field, paddle):
        def get_grid_point(coord):
            """Pixel coordinate -> grid coordinate"""
            return coord[0] // field.block_ws, (coord[1] - field.offset_y) // field.block_hs

        def get_pixel_point(coord):
            """Grid coordinate -> pixel coordinate"""
            return coord[0] * field.block_ws, coord[1] * field.block_hs + field.offset_y

        all_points = {}
        left, right, top, bottom = \
            self.pos[0], \
            self.pos[0] + self.surface.get_width(), \
            self.pos[1], \
            self.pos[1] + self.surface.get_height()
        quarter_w, quarter_h = self.surface.get_width() // 4, self.surface.get_height() // 4
        if self.direction == [-1, -1]:
            # left, top
            all_points['vertical'] = [[left, y] for y in range(top + 1, bottom - quarter_h)]
            all_points['horizontal'] = [[x, top] for x in range(left + 1, right - quarter_w)]
        elif self.direction == [1, -1]:
            # right, top
            all_points['vertical'] = [[right, y] for y in range(top + 1, bottom - quarter_h)]
            all_points['horizontal'] = [[x, top] for x in range(left + quarter_w, right)]
        elif self.direction == [1, 1]:
            # right, bot
            all_points['vertical'] = [[right, y] for y in range(top + quarter_h, bottom)]
            all_points['horizontal'] = [[x, bottom] for x in range(left + quarter_w, right)]
        elif self.direction == [-1, 1]:
            # left, bot
            all_points['vertical'] = [[left, y] for y in range(top + quarter_h, bottom)]
            all_points['horizontal'] = [[x, bottom] for x in range(left + 1, right - quarter_w)]

        hits = {'vertical': 0, 'horizontal': 0, 'paddle': 0}
        where = set()
        for flag, points in all_points.items():
            for point in points:
                point = tuple(point)
                if get_grid_point(point) in field.grid:
                    hits[flag] += 1
                    where.add(get_grid_point(point))

                elif point in paddle.col:
                    hits['paddle'] = -1 if paddle.col[point] in 'left' else 1

                elif point[0] >= self.window_w or point[0] <= 0 or point[1] <= 0:
                    hits[flag] += 1
                elif point[1] >= self.window_h:
                    return 'lose', ()

        if hits['paddle']:
            if hits['vertical']:
                self.direction[0] *= -1
                self.direction[1] *= -1
            else:
                self.direction = [hits['paddle'], -1]
            return 'paddle', ()

        if hits['vertical'] or hits['horizontal']:
            if len(where) == 3:
                a, b, c = where
                if a[0] != b[0] and a[1] != b[1]:
                    where.remove(c)
                elif a[0] != c[0] and a[1] != c[1]:
                    where.remove(b)
                elif b[0] != c[0] and b[1] != c[1]:
                    where.remove(a)
                self.direction[0] *= -1
                self.direction[1] *= -1
            elif len(where) == 2:
                a, b = where
                if a[0] == b[0]:
                    self.direction[0] *= -1
                elif a[1] == b[1]:
                    self.direction[1] *= -1
                else:
                    self.direction[0] *= -1
                    self.direction[1] *= -1
            else:
                v, h = hits['vertical'], hits['horizontal']

                if v > h:
                    self.direction[0] *= -1
                elif v < h:
                    self.direction[1] *= -1
                elif v == h:
                    self.direction[0] *= -1
                    self.direction[1] *= -1

            return 'field', {get_pixel_point(i) for i in where}

        return '', ()
