import pygame

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 200, 0, 0


class Menu:
    def __init__(self, window):
        self.window = window
        size1, size2 = int(self.window.get_width() * 0.15), int(self.window.get_width() * 0.1)
        self.text = [
            ["Breakout", pygame.font.SysFont(None, size1), WHITE, [0, int(self.window.get_height() * 0.09)], 'nil'],
            ["Play", pygame.font.SysFont(None, size2), WHITE, [0, int(self.window.get_height() * 0.45)], 'play'],
            ["Quit", pygame.font.SysFont(None, size2), WHITE, [0, int(self.window.get_height() * 0.6)], 'quit'],
        ]

        def set_x_pos(buttons):
            for button in buttons:
                msg, font = button[:2]
                surf = font.render(msg, True, WHITE)
                buttons[buttons.index(button)][3][0] = self.window.get_width() // 2 - surf.get_width() // 2
        set_x_pos(self.text)

        self.bounding_boxes = {}
        self.set_col()

    def set_col(self):
        for button in self.text[1:]:
            box = []
            msg, base, color, pos, action = button
            w, h = base.render(msg, True, color).get_size()
            for x in range(w):
                for y in range(h):
                    box.append([x + pos[0], y + pos[1]])
            self.bounding_boxes[action] = box

    def loop(self):
        pygame.mouse.set_visible(True)
        self.window.fill(BLACK)
        for text in self.text:
            msg, font, color, pos, action = text
            self.window.blit(font.render(msg, True, color), pos)

    def button_check(self, mouse_pos):
        for action, box in self.bounding_boxes.items():
            if list(mouse_pos) in box:
                if action in 'play':
                    return True
                elif action in 'quit':
                    quit()

    def button_highlight(self, mouse_pos):
        if list(mouse_pos) in self.bounding_boxes['play']:
            self.text[1][2] = RED
        else:
            self.text[1][2] = WHITE
        if list(mouse_pos) in self.bounding_boxes['quit']:
            self.text[2][2] = RED
        else:
            self.text[2][2] = WHITE
