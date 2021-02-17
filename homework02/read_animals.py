#!/usr/bin/env python3
import json
import random
import sys

def summary_stats(animals):
    
    assert isinstance(animals, list)
    
    head_count = {'snake' : 0, 'bull' : 0, 'lion' : 0, 'raven' : 0, 'bunny' : 0}
    arm_count = 0
    leg_count = 0
    tail_count = 0

    for animal in animals:
        this_head = animal['head']
        this_arms = animal['arms']
        this_legs = animal['legs']
        this_tail = animal['tail']

        assert isinstance(this_head, str)
        assert isinstance(this_arms, (int,float)) and not isinstance(this_arms,bool)
        assert isinstance(this_legs, (int,float)) and not isinstance(this_legs,bool)
        assert isinstance(this_tail, (int,float)) and not isinstance(this_tail,bool)

        head_count[this_head] = head_count[this_head] + 1

        arm_count += int(this_arms)
        leg_count += int(this_legs)
        tail_count += int(this_tail)

    avg_head = max(head_count, key=head_count.get)
    arm_count = int(arm_count/len(animals))
    leg_count = int(leg_count/len(animals))
    tail_count = int(tail_count/len(animals))

    avg_animal = {'head' : avg_head, 'arms' : arm_count, 'legs' : leg_count, 'tail' : tail_count}
    
    return avg_animal


def main():

    with open(sys.argv[1], 'r') as f:
        animals = json.load(f)

    animal = animals[random.randrange(len(animals))]
    print(f'Random animal: {animal}')

    avg_animal = summary_stats(animals)
    print(f'Average animal: {avg_animal}')

if __name__ == '__main__':
    main()
