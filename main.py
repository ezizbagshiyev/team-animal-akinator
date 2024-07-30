import pyodbc
import random
import os
import pyodbc
import random
from Config import *

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

def ask_random_question(animals, questions_attributes):
    if not questions_attributes:
        print("I am sorry, I could not guess your animal.")
        quit()

    # Randomly select a question
    question, attribute = random.choice(questions_attributes)
    questions_attributes.remove((question, attribute))  # Remove the selected question

    ans = input(question + "(y,n)").lower()
    value = True if ans == "y" else False

    filtered_animals = [animal for animal in animals if animal.get(attribute) == value]

    if len(filtered_animals) == 1:
        print("The animal you are thinking of is: " + filtered_animals[0]["Name"])
        quit()
    elif len(filtered_animals) == 0:
        print("I am sorry, I could not guess your animal.")
        quit()

    return filtered_animals

# Define questions and corresponding attributes
questions_attributes = questions_atr

animals = fetch_animals()

print("Please think of an animal and I will try to guess it.")

# Main game loop
while questions_attributes and animals:
    animals = ask_random_question(animals, questions_attributes)

conn.close()