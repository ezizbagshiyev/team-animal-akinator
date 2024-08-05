import os
import pyodbc
import random
from config import *

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
        print("I am sorry, I could not guess your animal.")
        quit()

    for animal in probabilities:
        probabilities[animal] /= total_prob

    return probabilities

def ask_random_question(animals, questions_attributes, initial_probabilities, conditional_probabilities, responses, threshold=0.75, error_tolerance=0.1):
    if not questions_attributes:
        print("I am sorry, I could not guess your animal.")
        quit()

    # Check if any animal has a significantly higher probability
    max_prob = max(initial_probabilities.values())
    best_guess = [animal for animal, prob in initial_probabilities.items() if prob == max_prob]

    if max_prob >= threshold and len(best_guess) == 1:
        print("The animal you are thinking of is: " + best_guess[0])
        quit()

    # Randomly select a question
    question, attribute = random.choice(questions_attributes)
    questions_attributes.remove((question, attribute))  # Remove the selected question

    ans = input(question + "(y,n)").lower()
    value = True if ans == "y" else False
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

print("Please think of an animal and I will try to guess it.")

# Main game loop
while questions_attributes and animals:
    animals, initial_probabilities = ask_random_question(animal_dict, questions_attributes, initial_probabilities, conditional_probabilities, responses)

conn.close()
