import os
import pyodbc
import pygame
import random
from config import *

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animal Guessing Game")

# Fonts
font = pygame.font.Font(None, font_size)

# Sound
#pygame.mixer.music.load("Theme-sound#1-Minecraft.mp3")
pygame.mixer.music.load("Music/Theme-sound#2-Stardew Valley.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Images
Panda_img = pygame.image.load("Pandapic/Panda_Idle.png")
Panda_img = pygame.transform.scale(Panda_img, (160, 220))
Panda_thinking = pygame.image.load("Pandapic/Panda_Thinking.png")
Panda_thinking = pygame.transform.scale(Panda_thinking, (160, 220))
Panda_happy = pygame.image.load("Pandapic/Panda_Happy.png")
Panda_happy = pygame.transform.scale(Panda_happy, (160, 220))
Panda_sad = pygame.image.load("Pandapic/Panda_Sad.png")
Panda_sad = pygame.transform.scale(Panda_sad, (160, 180))
bg_image = pygame.image.load('Background/background_image.jpg')
bg_image_fade = pygame.image.load('Background/background_image_fade.jpg')

#set Icon
icon = pygame.image.load("Background/icon.png")
pygame.display.set_icon(icon)

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
    """
    Fetches animal data from the database.

    Returns:
        list: A list of dictionaries containing animal data.
    """
    cursor.execute('SELECT * FROM Animals')
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Preload animal images
animal_images = {}
for animal in fetch_animals():
    for i in range(1, 4):
        image_path = f'animalpics/{animal["Name"]}{i}.jpg'
        if os.path.exists(image_path):
            animal_images[f'{animal["Name"]}{i}'] = pygame.image.load(image_path)

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

def draw_text(text, font, color, surface, rect):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
    surface.blit(textobj, textrect)

def draw_button(screen, color, rect, text, font, text_color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    draw_text(text, font, text_color, screen, rect)
    pygame.draw.rect(screen, black, rect, 2, border_radius=10)  # Add border for better visual feedback

def is_mouse_hovering(rect, mouse_pos):
    return rect[0] <= mouse_pos[0] <= rect[0] + rect[2] and rect[1] <= mouse_pos[1] <= rect[1] + rect[3]

def display_end_screen(message, animal_name=None):
    clock = pygame.time.Clock()
    rand_num = (random.randint(1, 3))
    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(bg_image_fade, (0, 0))
        draw_text(message, font, black, screen, (50, 200, 400, 50)) if animal_name else draw_text(message, font, black, screen,(50, 200, 400, 50))
        if animal_name:
            animal_pic = animal_images.get(f'{animal_name}{rand_num}')
            if animal_pic:
                draw_text(animal_name, font, black, screen, (screen_width // 2 - 60, 250, 120, 50))
                screen.blit(animal_pic, (screen_width // 2 - 150, 300))
                screen.blit(Panda_happy, (screen_width // 2 + 100, 300))
        else:
            screen.blit(Panda_sad, (screen_width // 2 - 80, 420))

        end_button_color = dark_red if is_mouse_hovering((*end_button_pos, button_width, button_height), mouse_pos) else red
        draw_button(screen, end_button_color, (*end_button_pos, button_width, button_height), "End", font, black)

        reply_button_color = dark_green if is_mouse_hovering((*reply_button_pos, button_width, button_height), mouse_pos) else green
        draw_button(screen, reply_button_color, (*reply_button_pos, button_width, button_height), "Again", font, black)

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
    clock = pygame.time.Clock()

    running = True

    try:
        while running:
            clock.tick(60)
            screen.blit(bg_image, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            if not game_started:
                start_button_color = dark_green if is_mouse_hovering((*start_button_pos, button_width, button_height), mouse_pos) else green
                sound_button_color = dark_red if is_mouse_hovering((*sound_button_pos, button_width, button_height), mouse_pos) else red

                draw_button(screen, start_button_color, (*start_button_pos, button_width, button_height), "Start", font, black)
                draw_button(screen, sound_button_color, (*sound_button_pos, button_width, button_height), "Sound", font, black)

            else:
                screen.blit(bg_image_fade, (0, 0))
                draw_text(question, font, black, screen, (50, 20, 400, 50))
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
                    if not game_started:
                        if is_mouse_hovering((*start_button_pos, button_width, button_height), mouse_pos):
                            game_started = True
                            question, attribute = ask_informative_question(animals, questions_attributes, responses)
                        elif is_mouse_hovering((*sound_button_pos, button_width, button_height), mouse_pos):
                            if pygame.mixer.music.get_busy():
                                pygame.mixer.music.stop()
                            else:
                                pygame.mixer.music.play(-1)
                    else:
                        if attribute is not None:
                            if is_mouse_hovering((*yes_button_pos, button_width, button_height), mouse_pos):
                                responses[attribute] = True
                            elif is_mouse_hovering((*no_button_pos, button_width, button_height), mouse_pos):
                                responses[attribute] = False
                            else:
                                continue  # Ignore clicks outside buttons

                            animals = [animal for animal in animals if animal.get(attribute) == responses[attribute]]
                            if not animals:
                                game_started = False
                                display_end_screen("No animals found.")
                            else:
                                probabilities = update_probabilities(animal_dict, initial_probabilities,
                                                                     conditional_probabilities, responses)
                                if len(animals) == 1:
                                    game_started = False
                                    display_end_screen("The animal you are thinking of is:", animals[0]["Name"])
                                else:
                                    question, attribute = ask_informative_question(animals, questions_attributes,responses)

                                    # Handle multiple candidates with similar probabilities
                                    top_probabilities = sorted(probabilities.values(), reverse=True)
                                    if len(top_probabilities) > 1 and top_probabilities[0] > 0.018:  # Threshold for chaing panda to "thinking"
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