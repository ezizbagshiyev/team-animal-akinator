import random

# Animal database
animal_dict = [
    {"animal":"Dog", "mammal":True, "pet":True, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":True, "swim":True, "petstore":True, "trees":False, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":False, "roar":False, "bark":True, "long_ears":False},

    {"animal":"Cat", "mammal":True, "pet":True, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":True, "swim":True, "petstore":True, "trees":False, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":True, "pouch":False, "sharp_teeth":True, "nocturnal":False, "ice":False, "carnivore":True, "stand":False, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Cow", "mammal":True, "pet":False, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":True, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":False, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Horse", "mammal":True, "pet":True, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":False, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Chicken", "mammal":True, "pet":True, "4_legs":False, "water":False, "wings":True, "feathers":True, "size":True, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":True, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":True, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Duck", "mammal":True, "pet":False, "4_legs":False, "water":False, "wings":True, "feathers":True, "size":True, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":True, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":True, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Rabbit", "mammal":True, "pet":True, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":True, "swim":True, "petstore":True, "trees":False, "reptile":False, "eaten":True, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":False, "roar":False, "bark":False, "long_ears":True},

    {"animal":"Elephant", "mammal":True, "pet":False, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":False, "roar":False, "bark":False, "long_ears":True},

    {"animal":"Lion", "mammal":True, "pet":False, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":True, "pouch":False, "sharp_teeth":True, "nocturnal":False, "ice":False, "carnivore":True, "stand":False, "roar":True, "bark":False, "long_ears":False},

    {"animal":"Kangaroo", "mammal":True, "pet":False, "4_legs":False, "water":False, "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":False, "pouch":True, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":True, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Bear", "mammal":True, "pet":False, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":True, "pouch":False, "sharp_teeth":True, "nocturnal":False, "ice":False, "carnivore":False, "stand":False, "roar":True, "bark":False, "long_ears":False},

    {"animal":"Deer", "mammal":True, "pet":False, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":True, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivor":False, "stand":False, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Owl", "mammal":True, "pet":False, "4_legs":False, "water":False, "wings":True, "feathers":True, "size":True, "swim":False, "petstore":False, "trees":True, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":True, "pouch":False, "sharp_teeth":False, "nocturnal":True, "ice":False, "carnivore":True, "stand":True, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Penguin", "mammal":True, "pet":False, "4_legs":False, "water":False, "wings":True, "feathers":True, "size":True, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":True, "carnivore":False, "stand":True, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Shark", "mammal":False, "pet":False, "4_legs":False, "water":True, "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":False, "poisonous":False, "webs":False, "predator":True, "pouch":False, "sharp_teeth":True, "nocturnal":False, "ice":False, "carnivore":True, "stand":False, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Snake", "mammal":False, "pet":True, "4_legs":False, "water":False, "wings":False, "feathers":False, "size":True, "swim":True, "petstore":True, "trees":True, "reptile":True, "eaten":False, "poisonous":True, "webs":False, "predator":True, "pouch":False, "sharp_teeth":True, "nocturnal":False, "ice":False, "carnivore":True, "stand":False, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Alligator", "mammal":False, "pet":False, "4_legs":True, "water":True , "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":True, "eaten":True, "poisonous":False, "webs":False, "predator":True, "pouch":False, "sharp_teeth":True, "nocturnal":False, "ice":False, "carnivore":True, "stand":False, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Pig", "mammal":True, "pet":False, "4_legs":True, "water":False, "wings":False, "feathers":False, "size":False, "swim":True, "petstore":False, "trees":False, "reptile":False, "eaten":True, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":False, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Spider", "mammal":False, "pet":True, "4_legs":False, "water":False, "wings":False, "feathers":False, "size":True, "swim":False, "petstore":True, "trees":True, "reptile":False, "eaten":False, "poisonous":False, "webs":True, "predator":True, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivore":False, "stand":False, "roar":False, "bark":False, "long_ears":False},

    {"animal":"Frog", "mammal":False, "pet":True, "4_legs":False, "water":True, "wings":False, "feathers":False, "size":True, "swim":True, "petstore":True, "trees":True, "reptile":True, "eaten":False, "poisonous":False, "webs":False, "predator":False, "pouch":False, "sharp_teeth":False, "nocturnal":False, "ice":False, "carnivor":False, "stand":False, "roar":False, "bark":False, "long_ears":False},

]

# Question database
questions = [
    {"question":"Is your animal a pet?", "attribute":"pet", "mammal":True, "reptile":True, "insect":True},
    {"question":"Is your animal a mammal?", "attribute":"mammal", "mammal":True, "reptile":False, "insect":False},
    {"question":"Is your animal a reptile?", "attribute":"reptile", "mammal":False, "reptile":True, "insect":False},
    {"question":"Does your animal have four legs?", "attribute":"4_legs", "mammal":True, "reptile":True, "insect":True},
    {"question":"Does your animal live in the water?", "attribute":"water", "mammal":True, "reptile":True, "insect":True},
    {"question":"Does your animal have wings?", "attribute":"wings", "mammal":True, "reptile":False, "insect":True},
    # Add more questions here as needed
]

# Asks a question and guesses animal at end.
def ask_question(answer, attribute):
    ans = answer.lower() == "y"
    to_remove_animal = [d for d in animal_dict if d[attribute] != ans]
    for i in to_remove_animal:
        animal_dict.remove(i)

    if len(animal_dict) == 1:
        print("The animal you are thinking of is: " + animal_dict[0]["animal"])
        quit()
    if len(animal_dict) == 0:
        print("I am sorry, I could not guess your animal.")
        return False
    return True

# Adds an animal to the database if the animal cannot be guessed
def add_new_animal(user_answers):
    new_animal = {}
    new_animal["animal"] = input("What animal were you thinking of? ")
    for question, attribute in user_answers.items():
        new_animal[attribute] = user_answers[question]
    animal_dict.append(new_animal)
    print(f"{new_animal['animal']} has been added to the database.")

print("Please think of an animal and I will try to guess it.")

# Shuffles the questions so they are asked in a random order
random.shuffle(questions)

# Keeps track of the users answers
user_answers = {}

# Loops through the questions and asks them
for question_dict in questions:
    question = question_dict["question"]
    attribute = question_dict["attribute"]

    # Skips irrelevant questions based on answers to previous questions
    if any(user_answers.get(attr) == True for attr in question_dict if attr in user_answers and not question_dict[attr]):
        continue

    ans = input(question + " (y/n) ")
    user_answers[attribute] = ans.lower() == 'y'
    if not ask_question(ans, attribute):
        add_new_animal(user_answers)
        break

