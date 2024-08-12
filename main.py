import os
import pyodbc
import random
import pygame
from config import *

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animal Guessing Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, font_size)

# Button dimensions
button_width = 100
button_height = 50

# Button positions
start_button_pos = (screen_width // 2 - button_width // 2, screen_height // 2)
yes_button_pos = (screen_width // 4 - button_width // 2, screen_height // 2)
no_button_pos = (3 * screen_width // 4 - button_width // 2, screen_height // 2)

# Database connection
db_file = 'animal-database.accdb'
if not os.path.exists(db_file):
    print(f"Warning: The database file {db_file} does not exist in the current directory.")
    exit()

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    rf'DBQ={os.path.abspath(db_file)};'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

def fetch_animals():
    cursor.execute('SELECT * FROM Animals')
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def calculate_conditional_probabilities(animals):
    attribute_probabilities = {}
    total_animals = len(animals)

    for animal in animals:
        for attribute, value in animal.items():
            if attribute not in attribute_probabilities:
                attribute_probabilities[attribute] = {"true": 0, "false": 0}
            if value:
                attribute_probabilities[attribute]["true"] += 1
            else:
                attribute_probabilities[attribute]["false"] += 1

    for attribute, counts in attribute_probabilities.items():
        attribute_probabilities[attribute]["true"] /= total_animals
        attribute_probabilities[attribute]["false"] /= total_animals

    return attribute_probabilities

def entropy(animals):
    from math import log2
    counts = {}
    for animal in animals:
        label = animal['Name']
        if label not in counts:
            counts[label] = 0
        counts[label] += 1

    entropy = 0
    for label in counts:
        prob_of_label = counts[label] / float(len(animals))
        entropy -= prob_of_label * log2(prob_of_label)

    return entropy

def information_gain(animals, attribute):
    yes_animals = [animal for animal in animals if animal[attribute]]
    no_animals = [animal for animal in animals if not animal[attribute]]

    if not yes_animals or not no_animals:
        return 0

    p_yes = len(yes_animals) / len(animals)
    p_no = len(no_animals) / len(animals)

    return entropy(animals) - p_yes * entropy(yes_animals) - p_no * entropy(no_animals)

def best_question(animals, questions_attributes):
    best_gain = 0
    best_question = None
    best_attribute = None

    for question, attribute in questions_attributes:
        gain = information_gain(animals, attribute)
        if gain > best_gain:
            best_gain = gain
            best_question = question
            best_attribute = attribute

    return best_question, best_attribute

def update_probabilities(animals, initial_probabilities, conditional_probabilities, responses, error_tolerance=0.1):
    probabilities = initial_probabilities.copy()

    for attribute, response in responses.items():
        for animal in probabilities.keys():
            p_b_given_a = 1 - error_tolerance if animals[animal].get(attribute) == response else error_tolerance
            p_a = initial_probabilities[animal]
            p_b = conditional_probabilities[attribute][str(response).lower()]

            if p_b > 0:
                probabilities[animal] = (p_b_given_a * p_a) / p_b

    total_prob = sum(probabilities.values())
    if total_prob == 0:
        # Handle the case where all probabilities are zero
        print("I am sorry, I could not guess your animal.")
        quit()

    for animal in probabilities:
        probabilities[animal] /= total_prob

    return probabilities

def ask_informative_question(animals, questions_attributes, responses):
    if not questions_attributes:
        print("I am sorry, I could not guess your animal.")
        quit()

    question, attribute = best_question(animals, questions_attributes)
    if question is None:
        print("I am sorry, I could not guess your animal.")
        quit()

    questions_attributes.remove((question, attribute))  # Remove the selected question

    return question, attribute

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main():
    animals = fetch_animals()
    animal_dict = {animal['Name']: animal for animal in animals}
    initial_probabilities = {animal['Name']: 1/len(animals) for animal in animals}
    conditional_probabilities = calculate_conditional_probabilities(animals)
    responses = {}
    questions_attributes = questions_atr.copy()

    running = True
    game_started = False
    question, attribute = None, None

    while running:
        screen.fill(white)

        if not game_started:
            pygame.draw.rect(screen, green, (*start_button_pos, button_width, button_height))
            draw_text("Start", font, black, screen, start_button_pos[0] + 20, start_button_pos[1] + 12)
        else:
            draw_text(question, font, black, screen, 50, 20)
            pygame.draw.rect(screen, green, (*yes_button_pos, button_width, button_height))
            draw_text("Yes", font, black, screen, yes_button_pos[0] + 30, yes_button_pos[1] + 10)
            pygame.draw.rect(screen, red, (*no_button_pos, button_width, button_height))
            draw_text("No", font, black, screen, no_button_pos[0] + 30, no_button_pos[1] + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if not game_started and start_button_pos[0] <= mouse_pos[0] <= start_button_pos[0] + button_width and start_button_pos[1] <= mouse_pos[1] <= start_button_pos[1] + button_height:
                    game_started = True
                    question, attribute = ask_informative_question(animals, questions_attributes, responses)
                elif game_started:
                    if yes_button_pos[0] <= mouse_pos[0] <= yes_button_pos[0] + button_width and yes_button_pos[1] <= mouse_pos[1] <= yes_button_pos[1] + button_height:
                        responses[attribute] = True
                    elif no_button_pos[0] <= mouse_pos[0] <= no_button_pos[0] + button_width and no_button_pos[1] <= mouse_pos[1] <= no_button_pos[1] + button_height:
                        responses[attribute] = False

                    animals = [animal for animal in animals if animal.get(attribute) == responses[attribute]]
                    if len(animals) == 1:
                        print("The animal you are thinking of is: " + animals[0]["Name"])

                        screen.fill(white)
                        draw_text("The animal you are thinking of is:", font, black, screen, 50, 200)
                        draw_text(animals[0]["Name"], font, black, screen, screen_width // 2 - 40, 250)
                        pygame.display.flip()
                        pygame.time.wait(5000)
                        running = False

                    elif len(animals) == 0:
                        print("apple")
                        quit()

                    else:
                        question, attribute = ask_informative_question(animals, questions_attributes, responses)

        pygame.display.flip()

    pygame.quit()
    conn.close()

if __name__ == "__main__":
    main()