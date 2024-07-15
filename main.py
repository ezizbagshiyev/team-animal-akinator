import pygame
import sys

class GameMenu:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 640, 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)
        self.menu_options = ['Start', 'Options', 'Exit']
        self.option_functions = {
            'Start': lambda: print("Game Started"),
            'Options': lambda: print("Option Settings"),
            'Exit': sys.exit
        }

    def draw_menu(self):
        self.screen.fill(self.black)
        for i, option in enumerate(self.menu_options):
            text = self.font.render(option, True, self.white)
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, 150 + i * 50))
        pygame.display.flip()

    def main_menu(self):
        while True:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    for i, option in enumerate(self.menu_options):
                        text = self.font.render(option, True, self.white)
                        text_rect = text.get_rect(center=(self.screen_width // 2, 150 + i * 50))
                        if text_rect.collidepoint(x, y):
                            self.option_functions[option]()

            pygame.display.update()

    def run(self):
        self.main_menu()

# Instantiate and run the game menu
if __name__ == "__main__":
    game_menu = GameMenu()
    game_menu.run()