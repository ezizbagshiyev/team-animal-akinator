# Configuration settings for the game

# Screen settings
screen_width = 510
screen_height = 600

# Paths to resources
background_image = ""

# Font settings
font_size = 36

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
dark_green = (0, 180, 0)
dark_red = (160, 0, 0)

# Button dimensions
button_width = 100
button_height = 50

# Button positions
start_button_pos = (screen_width // 2 - button_width // 2, screen_height // 2)
yes_button_pos = (screen_width // 4 - button_width // 2, screen_height // 2)
no_button_pos = (3 * screen_width // 4 - button_width // 2, screen_height // 2)
reply_button_pos = (screen_width - 120, 10)
sound_button_pos = (screen_width - 120, 10)
end_button_pos = (screen_width - 480, 10)


questions_atr = [
    ("Is your animal a pet?", "IsPet"),
    ("Does your animal have four legs?", "FourLegs"),
    ("Does your animal live in the water?", "LivesWater"),
    ("Does your animal have a tail?", "HasTail"),
    ("Does your animal have fur?", "HasFur"),
    ("Does your animal have scales?", "HasScales"),
    ("Does your animal have feathers?", "HasFeathers"),
    ("Does your animal have hooves?", "HasHooves"),
    ("Does your animal have wings?", "HasWings"),
    ("Does your animal have a beak?", "HasBeak"),
    ("Is your animal a mammal?", "IsMammal"),
    ("Does your animal live in water?", "LivesWater"),
    ("Is your animal a carnivore?", "IsCarnivore"),
    ("Is your animal an herbivore?", "IsHerbivore"),
    ("Does your animal fly?", "HasWings"),
    ("Does your animal lay eggs?", "LaysEggs"),
    ("Does your animal have scales?", "HasScales"),
    ("Does your animal live in trees?", "LivesTrees"),
    ("Is the animal larger than a human?", "LargerThanHuman"),
    ("Is the animal smaller than a cat?", "SmallerThanCat"),
    ("Does the animal have a tail?", "HasTail"),
    ("Is the animal commonly kept as a pet?", "IsPet"),
    ("Does the animal live in the wild?", "LivesLand"),
    ("Is the animal native to Africa?", "NativeAfrica"),
    ("Is the animal native to North America?", "NativeNAmerica"),
    ("Does the animal have stripes?", "HasStripes"),
    ("Does the animal have spots?", "HasSpots"),
    ("Is the animal known for its speed?", "KnownForSpeed"),
    ("Is the animal nocturnal?", "Nocturnal"),
    ("Is the animal a bird?", "IsBird"),
    ("Is the animal a reptile?", "IsReptile"),
    ("Is the animal an amphibian?", "IsAmphibian"),
    ("Is the animal a fish?", "IsFish"),
    ("Is the animal an insect?", "IsInsect"),
    ("Is the animal an arthropod?", "IsArthropod"),
    ("Does the animal live on land?", "LivesLand"),
    ("Does the animal live in the desert?", "LivesDesert"),
    ("Does the animal live in the forest?", "LivesForest"),
    ("Does the animal live in the mountains?", "LivesMtns"),
    ("Does the animal live in the grasslands?", "LivesGrass"),
    ("Does the animal live in the ocean?", "LivesOcean"),
    ("Does the animal live in freshwater?", "LivesFresh"),
    ("Does the animal live in caves?", "LivesCaves"),
    ("Does the animal live underground?", "LivesUnder"),
    ("Does the animal live in a savanna?", "LivesSavana"),
    ("Does the animal live in the Arctic or Antarctic?", "LivesArctic"),
    ("Does the animal have feathers?", "HasFeathers"),
    ("Does the animal have a shell?", "HasShell"),
    ("Does the animal have a long neck?", "LongNeck"),
    ("Does the animal have horns or antlers?", "HornsAntlers"),
    ("Does the animal have tusks?", "HasTusks"),
    ("Does the animal have a beak?", "HasBeak"),
    ("Does the animal have claws?", "HasClaws"),
    ("Does the animal have hooves?", "HasHooves"),
    ("Does the animal have gills?", "HasGills"),
    ("Does the animal have fins?", "HasFins"),
    ("Is the animal very small?", "VerySmall"),
    ("Is the animal an omnivore?", "IsOmnivore"),
    ("Does the animal eat insects?", "EatsInsects"),
    ("Does the animal eat plants?", "EatsPlants"),
    ("Does the animal eat fish?", "EatsFish"),
    ("Does the animal eat meat?", "EatsMeat"),
    ("Does the animal eat fruits?", "EatsFruits"),
    ("Does the animal eat nuts and seeds?", "EatsNuts"),
    ("Does the animal scavenge for food?", "Scavenges"),
    ("Is the animal diurnal?", "Diurnal"),
    ("Does the animal live in groups?", "Groups"),
    ("Is the animal migratory?", "Migratory"),
    ("Is the animal territorial?", "Territorial"),
    ("Does the animal hibernate?", "Hibernates"),
    ("Does the animal use camouflage?", "Camouflages"),
    ("Does the animal burrow?", "Burrows"),
    ("Does the animal build nests?", "BuildsNests"),
    ("Is the animal known for its strength?", "KnownForStrength"),
    ("Is the animal known for its intelligence?", "KnownForIntelligence"),
    ("Does the animal exhibit playful behavior?", "Playful"),
    ("Does the animal give live birth?", "LiveBirth"),
    ("Does the animal have a pouch?", "Pouch"),
    ("Does the animal care for its young?", "CaresYoung"),
    ("Does the animal have a specific mating season?", "MatingSeason"),
    ("Is the animal native to Asia?", "NativeAsia"),
    ("Is the animal native to Australia?", "NativeAustralia"),
    ("Is the animal native to South America?", "NativeSAmerica"),
    ("Is the animal native to Europe?", "NativeEurope"),
    ("Is the animal native to Antarctica?", "NativeAntarctica"),
    ("Does the animal inhabit multiple continents?", "MultiContinent"),
    ("Is the animal commonly found in zoos?", "FoundZoos"),
    ("Is the animal used for work?", "UsedWork"),
    ("Is the animal used for food?", "UsedFood"),
    ("Is the animal endangered?", "Endangered"),
    ("Is the animal protected by law?", "Protected"),
    ("Is the animal venomous?", "Venomous"),
    ("Is the animal bioluminescent?", "Bioluminescent"),
    ("Does the animal have a symbiotic relationship with another species?", "Symbiotic"),
    ("Is the animal vocal?", "Vocal"),
    ("Does the animal have significant cultural or mythological significance?", "CulturalSignificance"),
    ("Is the animal known for a specific physical adaptation?", "Adaptation"),
    ("Does the animal undergo metamorphosis?", "Metamorphosis"),
    ("Is the animal found in urban areas?", "Urban"),
    ("Does the animal have a unique way of moving?", "Movement"),
    ("Is the animal a predator?", "Predator"),
    ("Is the animal preyed upon by many other animals?", "Prey"),
    ("Does the animal have a long lifespan?", "LongLifespan"),
    ("Is the animal featured in children’s stories or educational materials?", "ChildStories"),
    ("Is the animal imaginary?", "Imaginary"),
    ("Can the animal swim?", "CanSwim"),
    ("Is the animal found in pet stores?", "PetStores"),
    ("Is the animal eaten by humans?", "EatenByHumans"),
    ("Is the animal poisonous?", "Poisonous"),
    ("Does the animal create webs?", "CreatesWebs"),
    ("Does the animal have sharp teeth?", "SharpTeeth"),
    ("Does the animal live on ice?", "LivesOnIce"),
    ("Does the animal have two legs?", "TwoLegs"),
    ("Does the animal roar?", "Roars"),
    ("Does the animal bark?", "Barks"),
    ("Does the animal have long ears?", "LongEars")
]
