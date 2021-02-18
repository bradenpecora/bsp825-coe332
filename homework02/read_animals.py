#!/usr/bin/env python3
import json
import random
import sys

def summary_stats(animals):
    """
    Takes in a list of dictionaries.
    Each dictionary must contain all of the following keys:
        'head': must have a string value equivalent to any of the following:
                    'snake', 'bull', 'lion', 'raven', or bunny
        'arms': an integer. floats will be typecasted to int.
        'legs': an integer. floats will be typecasted to int.
        'tail': an integer. floats will be typecasted to int.

    Function returns a dictionary containing the following:
        'head': The mode of the heads across the input list.
        'arms': The mean of the arms across the input list, rounded down to the nearest integer.
        'legs': The mean of the legs across the input list, rounded down to the nearest integer.
        'tail': The mean of the tails across the input list, rounded down to the nearest integer.
    """
    assert isinstance(animals, list)
    
    head_count = {'snake' : 0, 'bull' : 0, 'lion' : 0, 'raven' : 0, 'bunny' : 0}
    arm_count = 0
    leg_count = 0
    tail_count = 0

    for animal in animals:
        assert isinstance(animal, dict)
        
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
        animal_dict = json.load(f)

    rand_animal = random.choice(animal_dict['animals'])
    print(f'Random Animal: {rand_animal}')

    avg_animal = summary_stats(animal_dict['animals'])
    print(f'Average animal: {avg_animal}')

if __name__ == '__main__':
    main()
