import pygame
import sys
from config import *

class GameMenu:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = screen_width, screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load(background_image)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.font = pygame.font.Font(None, font_size)
        self.menu_options = menu_options
        self.option_functions = {
            'Start': self.start_game,
            'Options': lambda: print("Option Settings"),
            'Exit': sys.exit
        }
        self.option_rects = []

    def draw_menu(self):
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

    def start_game(self):
        game = AnimalAkinator(self.screen, self.font)
        game.display_question()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    if game.yes_button_rect.collidepoint(x, y):
                        game.handle_answer("yes")
                    elif game.no_button_rect.collidepoint(x, y):
                        game.handle_answer("no")
                pygame.display.update()


    def main_menu(self):
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


class AnimalAkinator:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.current_question_index = 0
        self.setup_buttons()

    def setup_buttons(self):
        # Define button dimensions and positions
        button_width, button_height = 100, 50
        screen_width, screen_height = self.screen.get_size()

        # Yes Button
        self.yes_button_rect = pygame.Rect(
            (screen_width // 2 - button_width // 2, screen_height // 2 + 60),
            (button_width, button_height)
        )

        # No Button
        self.no_button_rect = pygame.Rect(
            (screen_width // 2 - button_width // 2, screen_height // 2 + 120),
            (button_width, button_height)
        )

    def display_question(self):
        question = questions[self.current_question_index]["question"]
        text = self.font.render(question, True, (0, 0, 0))
        self.screen.fill((255, 255, 255))  # Clear screen with white
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        
        # Draw yes/no buttons
        pygame.draw.rect(self.screen, (0, 255, 0), self.yes_button_rect)  # Green button for 'Yes'
        pygame.draw.rect(self.screen, (255, 0, 0), self.no_button_rect)   # Red button for 'No'
        
        yes_text = self.font.render("Yes", True, (0, 0, 0))
        no_text = self.font.render("No", True, (0, 0, 0))
        self.screen.blit(yes_text, (self.yes_button_rect.centerx - yes_text.get_width() // 2, self.yes_button_rect.centery - yes_text.get_height() // 2))
        self.screen.blit(no_text, (self.no_button_rect.centerx - no_text.get_width() // 2, self.no_button_rect.centery - no_text.get_height() // 2))
        
        pygame.display.flip()

    def handle_answer(self, answer):
        current_question = questions[self.current_question_index]
        if answer == "yes":
            next_index = current_question.get("yes")
        else:
            next_index = current_question.get("no")

        if isinstance(next_index, int):
            self.current_question_index = next_index
            self.display_question()
        else:
            # End of the game
            self.end_game(next_index)

    def end_game(self, result):
        text = self.font.render(result, True, (0, 0, 0))
        self.screen.fill((255, 255, 255))  # Clear screen with white
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before returning to the main menu



if __name__ == "__main__":
    game_menu = GameMenu()
    game_menu.run()