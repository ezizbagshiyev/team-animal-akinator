import pygame
import sys
from config import *

class GameMenu:
    def __init__(self): # Initialize the game menu
        pygame.init()
        self.screen_width, self.screen_height = screen_width, screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) # Set the screen size
        self.background = pygame.image.load(background_image)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height)) # Set the background image
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.font = pygame.font.Font(None, font_size) # Set the font
        self.menu_options = menu_options # Set the menu options
        self.option_functions = {
            'Start': lambda: print("Game Started"),
            'Options': lambda: print("Option Settings"),
            'Exit': sys.exit
        } # Set the functions for each menu option
        self.option_rects = []  # Store the menu option rectangles

    def draw_menu(self): # Draw the main menu
        self.screen.blit(self.background, (0, 0))
        self.option_rects.clear()
        menu_height = len(self.menu_options) * 50
        start_y = (self.screen_height - menu_height) // 2

        for i, option in enumerate(self.menu_options):
            text = self.font.render(option, True, self.black)
            text_x = self.screen_width // 2 - text.get_width() // 2
            text_y = start_y + i * 50
            text_rect = text.get_rect(center=(self.screen_width // 2, text_y))
            self.option_rects.append(text_rect)
            self.screen.blit(text, text_rect.topleft)
        pygame.display.flip()

    def main_menu(self): # Main menu loop
        while True:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    for rect, option in zip(self.option_rects, self.menu_options):
                        if rect.collidepoint(x, y):
                            self.option_functions[option]()

            pygame.display.update()

    def run(self):
        self.main_menu()

if __name__ == "__main__":
    game_menu = GameMenu()
    game_menu.run()