import pygame

color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_yellow = (255, 255, 0)


class Menu:
    def __init__(self, surface, window_dimensions, message_func):
        self.surface = surface
        self.message = message_func
        self.window_dimensions = window_dimensions
        self.current_state = 'main'  # main, how
        self.buttons = {
            'play': [color_yellow, self.func1],
            'how': [color_white, self.func2],
            'quit': [color_white, self.func3],
        }
        self.buttons_list = ['play', 'how', 'quit']
        self.current_selection = 0
        self.play_status = False

    def func1(self):
        self.play_status = True

    def func2(self):
        self.current_state = 'how'

    @staticmethod
    def func3():
        pygame.quit()
        quit()

    def highlight(self, direction):
        if 'down' in direction:
            if self.current_selection == 2:
                self.current_selection = 0
            else:
                self.current_selection += 1
        elif 'up' in direction:
            if self.current_selection == 0:
                self.current_selection = 2
            else:
                self.current_selection -= 1

        for button in self.buttons_list:
            self.buttons[button][0] = color_white
        self.buttons[self.buttons_list[self.current_selection]][0] = color_yellow

    def activate(self):
        self.buttons[self.buttons_list[self.current_selection]][1]()

    def back(self):
        self.current_state = 'main'

    def render(self):
        if 'main' in self.current_state:
            self.surface.fill(color_black)
            self.message('Tetris', 4, (255, 255, 255), center='x', offset_arg=(0, 1))
            self.message('Play Game', 2, self.buttons['play'][0], center='x', offset_arg=(0, 6))
            self.message('How to Play', 2, self.buttons['how'][0], center='x', offset_arg=(0, 8))
            self.message('Quit', 2, self.buttons['quit'][0], center='x', offset_arg=(0, 10))
        elif 'how' in self.current_state:
            self.surface.fill(color_black)
            self.message('LEFT and RIGHT to move', 2, (255, 255, 255), center='x', offset_arg=(0, 2))
            self.message('UP to rotate', 2, (255, 255, 255), center='x', offset_arg=(0, 5))
            self.message('DOWN to drop', 2, (255, 255, 255), center='x', offset_arg=(0, 8))
            self.message('ENTER to pause game', 2, (255, 255, 255), center='x', offset_arg=(0, 11))
            self.message('Press ESCAPE to return to menu', 2, (255, 255, 255), center='x', offset_arg=(0, 16))
