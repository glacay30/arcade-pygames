import pygame
import assets as a


class Menu:
    def __init__(self, surface, message_func):
        self.surface = surface
        self.message = message_func
        self.current_state = 'main'  # main, how
        self.buttons = {
            'play': [a.color_yellow, self.func1],
            'how': [a.color_white, self.func2],
            'quit': [a.color_white, self.func3],
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
            self.buttons[button][0] = a.color_white
        self.buttons[self.buttons_list[self.current_selection]][0] = a.color_yellow

    def activate(self):
        self.buttons[self.buttons_list[self.current_selection]][1]()

    def back(self):
        self.current_state = 'main'

    def render(self):
        if 'main' in self.current_state:
            self.surface.fill(a.color_black)
            self.message('Tetris', pos=[60, 10], color=a.color_white, size=60)
            self.message('Play Game', pos=[50, 80], color=self.buttons['play'][0])
            self.message('How to Play', pos=[43, 110], color=self.buttons['how'][0])
            self.message('Quit', pos=[90, 140], color=self.buttons['quit'][0])
        elif 'how' in self.current_state:
            self.surface.fill(a.color_black)
            self.message('A, S, D to move block', pos=[10, 10], color=a.color_white, size=25)
            self.message('LEFT and RIGHT to rotate', pos=[10, 40], color=a.color_white, size=25)
            self.message('SPACE to drop block', pos=[10, 70], color=a.color_white, size=25)
            self.message('T to pause game', pos=[10, 100], color=a.color_white, size=25)
            self.message('ESCAPE to return to menu', pos=[10, 150], color=a.color_white, size=25)
