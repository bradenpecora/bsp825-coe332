import json
import random

with open('animals.json','r') as f:
    animals = json.load(f)

animal = animals[random.randrange(len(animals))]
print(animal)