import os
import pyodbc
import random
from config import *
import pygame
pygame.init()
import time

db_file = 'Animal-Database.accdb'
# Used to verify the database file path
if not os.path.exists(db_file):
    print(f"Warning: The database file {db_file} does not exist in the current directory.")
    exit()

# Connect to the database
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

font = pygame.font.Font(None, 74)
SCREEM_WIDTH=1280
SCREEN_HEIGHT=720

screen = pygame.display.set_mode((SCREEM_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Akinator")

start_img= pygame.image.load('start_btn.png').convert_alpha()
exit_img= pygame.image.load('exit_btn.png').convert_alpha()
yes_img= pygame.transform.scale(pygame.image.load('yes.png').convert_alpha(),(350,350))
no_img= pygame.transform.scale(pygame.image.load('no.png').convert_alpha(),(250,250))
class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False

    def draw(self):
        action= False
        pos= pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked==False:
                self.clicked=True
                action=True 
        if pygame.mouse.get_pressed()[0] == 0:
                self.clicked=False

        screen.blit(self.image,(self.rect.x, self.rect.y))
        return action

start_button= Button(500,280,start_img)
exit_button= Button(1040,0,exit_img)
yes_button= Button(200,280,yes_img)
no_button= Button(800,280,no_img)

#game
run=True
run2=False
while run:

    screen.fill((202,228,241)) 
    screen.blit(font.render("Techwise", True, (255, 255, 255)), (100, 100))
    if start_button.draw():
    
        run2=True
        run=False
    if exit_button.draw():
        run=False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False 
    pygame.display.update()



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
        screen.fill((53,27,14))
        screen.blit(font.render("I am sorry, I could not guess your animal", True, (255, 255, 255)), (100, 180))
        pygame.display.flip()
        time.sleep(5)  # Wait for 3 seconds before quitting
        pygame.quit()

    for animal in probabilities:
        probabilities[animal] /= total_prob

    return probabilities

def ask_random_question(animals, questions_attributes, initial_probabilities, conditional_probabilities, responses, threshold=0.75, error_tolerance=0.1):
    if not questions_attributes:
        screen.fill((53,27,14))
        screen.blit(font.render("I am sorry, I could not guess your animal", True, (255, 255, 255)), (100, 180))
        pygame.display.flip()
        time.sleep(5)  
        pygame.quit()

    # Check if any animal has a significantly higher probability
    max_prob = max(initial_probabilities.values())
    best_guess = [animal for animal, prob in initial_probabilities.items() if prob == max_prob]

    if max_prob >= threshold and len(best_guess) == 1:
        screen.fill((53,27,14))
        screen.blit(font.render(f"The animal you are thinking of is: {best_guess[0]}", True, (255, 255, 255)), (100, 180))
        pygame.display.flip()
        time.sleep(5) 
        pygame.quit()

    # Randomly select a question
    question, attribute = random.choice(questions_attributes)
    questions_attributes.remove((question, attribute))  # Remove the selected question
    run3=True
    while run3:
        screen.fill((53,27,14))
        screen.blit(font.render(question, True, (255, 255, 255)), (100, 180))

        if yes_button.draw():
            value = True
            run3 = False
        if no_button.draw():
            value = False
            run3 = False
        if exit_button.draw():
            pygame.quit()
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        
        pygame.display.flip()

    responses[attribute] = value


    updated_probabilities = update_probabilities(animals, initial_probabilities, conditional_probabilities, responses, error_tolerance)

    return animals, updated_probabilities

# Define questions and corresponding attributes
questions_attributes = questions_atr

animals = fetch_animals()

# Convert list of animals to a dictionary with animal names as keys
animal_dict = {animal['Name']: animal for animal in animals}

# Initial probabilities (equal for all animals)
initial_probabilities = {animal['Name']: 1/len(animals) for animal in animals}

# Calculate conditional probabilities
conditional_probabilities = calculate_conditional_probabilities(animals)

responses = {}

while run2:
    screen.fill((53,27,14)) 
    screen.blit(font.render("Please think of an animal and I will try to guess it.", True, (255, 255, 255)), (10, 250))
    pygame.display.flip()
    time.sleep(3)
    while questions_attributes and animals:
        animals, initial_probabilities = ask_random_question(animal_dict, questions_attributes, initial_probabilities, conditional_probabilities, responses)
        
        if exit_button.draw():
            run2=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run2=False
    

    if exit_button.draw():
        run2=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run2=False

    pygame.display.update()

pygame.quit()
conn.close()
