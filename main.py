import os
import pyodbc
import pygame
from config import *

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animal Guessing Game")

# Fonts
font = pygame.font.Font(None, font_size)

# Sound
pygame.mixer.music.load("Theme-sound#2-Stardew Valley.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Images
image_size = (200, 200)
Animal_img = pygame.image.load("img.png")
Animal_img = pygame.transform.scale(Animal_img, image_size)

# Panda Img
Panda_img = pygame.image.load("Panda_Idle.png")
Panda_img = pygame.transform.scale(Panda_img, (160, 220))
Panda_thinking = pygame.image.load("Panda_Thinking.png")
Panda_thinking = pygame.transform.scale(Panda_thinking, (160, 220))

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
        if attribute is None:
            continue
        for animal in probabilities.keys():
            p_b_given_a = 1 - error_tolerance if animals[animal].get(attribute) == response else error_tolerance
            p_a = initial_probabilities[animal]
            p_b = conditional_probabilities.get(attribute, {}).get(str(response).lower(), 0)

            if p_b > 0:
                probabilities[animal] = (p_b_given_a * p_a) / p_b

    total_prob = sum(probabilities.values())
    if total_prob == 0:
        print("total probability reach 0.")  # Debugging output
        game_started = False
        display_end_screen("No animals found.")
        running = False
        quit()

    for animal in probabilities:
        probabilities[animal] /= total_prob

    return probabilities

def ask_informative_question(animals, questions_attributes, responses):
    if not questions_attributes:
        print("No more question attributes.")  # Debugging output
        game_started = False
        display_end_screen("No animals found.")
        running = False
        quit()

    question, attribute = best_question(animals, questions_attributes)
    if question is None:
        print("No animals found after filtering.")  # Debugging output
        game_started = False
        display_end_screen("No animals found.")
        running = False
        quit()

    return question, attribute

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(screen, color, rect, text, font, text_color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    draw_text(text, font, text_color, screen, rect[0] + 20, rect[1] + 12)

def is_mouse_hovering(rect, mouse_pos):
    return rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]

def display_end_screen(message, animal_name=None):
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(white)
        draw_text(message, font, black, screen, 50, 200) if animal_name else draw_text(message, font, black, screen, 150, 200)
        if animal_name:
            draw_text(animal_name, font, black, screen, screen_width // 2 - 60, 250)
            screen.blit(Animal_img, (screen_width // 2 - 100, 300))

        end_button_color = dark_red if is_mouse_hovering((*end_button_pos, button_width, button_height), mouse_pos) else red
        draw_button(screen, end_button_color, (*end_button_pos, button_width, button_height), "End", font, black)

        reply_button_color = dark_green if is_mouse_hovering((*reply_button_pos, button_width, button_height), mouse_pos) else green
        draw_button(screen, reply_button_color, (*reply_button_pos, button_width, button_height), "Reply", font, black)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_mouse_hovering((*end_button_pos, button_width, button_height), mouse_pos):
                    pygame.quit()
                    exit()
                elif is_mouse_hovering((*reply_button_pos, button_width, button_height), mouse_pos):
                    main()


def main():
    # Initialize variables
    animals = fetch_animals()
    animal_dict = {animal['Name']: animal for animal in animals}
    initial_probabilities = {animal['Name']: 1 / len(animals) for animal in animals}
    conditional_probabilities = calculate_conditional_probabilities(animals)
    responses = {}
    questions_attributes = questions_atr.copy()
    game_started = False
    question = None
    attribute = None
    panda_img_to_display = Panda_img

    running = True

    try:
        while running:
            screen.fill(white)
            mouse_pos = pygame.mouse.get_pos()

            if not game_started:
                start_button_color = dark_green if is_mouse_hovering((*start_button_pos, button_width, button_height), mouse_pos) else green
                sound_button_color = dark_red if is_mouse_hovering((*sound_button_pos, button_width, button_height), mouse_pos) else red

                draw_button(screen, start_button_color, (*start_button_pos, button_width, button_height), "Start", font, black)
                draw_button(screen, sound_button_color, (*sound_button_pos, button_width, button_height), "Sound", font, black)

            else:
                draw_text(question, font, black, screen, 50, 20)
                yes_button_color = dark_green if is_mouse_hovering((*yes_button_pos, button_width, button_height), mouse_pos) else green
                no_button_color = dark_red if is_mouse_hovering((*no_button_pos, button_width, button_height), mouse_pos) else red

                draw_button(screen, yes_button_color, (*yes_button_pos, button_width, button_height), "Yes", font, black)
                draw_button(screen, no_button_color, (*no_button_pos, button_width, button_height), "No", font, black)

                screen.blit(panda_img_to_display, (screen_width // 2 - 80, 70))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not game_started and is_mouse_hovering((*start_button_pos, button_width, button_height), mouse_pos):
                        game_started = True
                        question, attribute = ask_informative_question(animals, questions_attributes, responses)
                    elif not game_started and is_mouse_hovering((*sound_button_pos, button_width, button_height), mouse_pos):
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()
                        else:
                            pygame.mixer.music.play(-1)
                    elif game_started:
                        if is_mouse_hovering((*yes_button_pos, button_width, button_height), mouse_pos):
                            responses[attribute] = True
                        elif is_mouse_hovering((*no_button_pos, button_width, button_height), mouse_pos):
                            responses[attribute] = False

                        if attribute is not None:
                            print(f"Filtering animals with attribute '{attribute}' = {responses[attribute]}")  # Debugging output

                            # Filter the animals based on the current response
                            animals = [animal for animal in animals if animal.get(attribute) == responses[attribute]]

                            print(f"Animals remaining: {len(animals)}")  # Debugging output

                            # If no animals match the criteria, set animals to an empty list
                            if not animals:
                                animals = []

                            # Check if no animals remain
                            if len(animals) == 0:
                                print("No animals found after filtering.")  # Debugging output
                                game_started = False
                                display_end_screen("No animals found.")
                            else:
                                # Update probabilities
                                probabilities = update_probabilities(animal_dict, initial_probabilities, conditional_probabilities, responses)

                                if len(animals) == 1:
                                    game_started = False
                                    print(f"Animal identified: {animals[0]['Name']}")  # Debugging output
                                    display_end_screen("The animal you are thinking of is:", animals[0]["Name"])
                                elif len(animals) > 1:
                                    # Update question after each response
                                    question, attribute = ask_informative_question(animals, questions_attributes, responses)

                                    # Handle multiple candidates with similar probabilities
                                    top_probabilities = sorted(probabilities.values(), reverse=True)
                                    if len(top_probabilities) > 1 and (top_probabilities[0] - top_probabilities[1]) > 0.00001:  # Threshold for "thinking"
                                        # Switch to Panda_thinking if the top probability is significantly higher
                                        panda_img_to_display = Panda_thinking
                                    else:
                                        panda_img_to_display = Panda_img  # Otherwise, show the idle panda
    except KeyboardInterrupt:
        print("Game interrupted by user.")
    finally:
        pygame.quit()
        conn.close()

if __name__ == "__main__":
    main()
