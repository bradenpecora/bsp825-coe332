import json
import random
import petname

head_options = ['snake', 'bull', 'lion', 'raven', 'bunny']

animals = []

for i in range(20):
    animals.append( {} )
    animals[i]['head'] = head_options[random.randrange(len(head_options))]
    animals[i]['body'] = petname.Name() + "-" + petname.Name()
    animals[i]['arms'] = random.randrange(2,11,2)
    animals[i]['legs'] = random.randrange(3,13,3)
    animals[i]['tail'] = animals[i]['arms'] + animals[i]['legs']

with open('animals.json', 'w') as out:
    json.dump(animals, out, indent=2)