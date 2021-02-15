#!/usr/bin/env python3
import json
import random
import sys

def summary_stats(animals):
    head_count = {'snake' : 0, 'bull' : 0, 'lion' : 0, 'raven' : 0, 'bunny' : 0}
    arm_count = 0
    leg_count = 0
    tail_count = 0

    for animal in animals:
        head = animal['head']
        head_count[head] = head_count[head] + 1

        arm_count += animal['arms']
        leg_count += animal['legs']
        tail_count += animal['tail']

    avg_head = max(head_count, key=head_count.get)
    arm_count = arm_count/len(animals)
    leg_count = leg_count/len(animals)
    tail_count = tail_count/len(animals)

    avg_animal = {'head' : avg_head, 'arms' : arm_count, 'legs' : leg_count, 'tail' : tail_count}
    
    return avg_animal


def main():

    with open(sys.argv[1], 'r') as f:
        animals = json.load(f)

    # animal = animal_dict[random.randrange(len(animal_dict))]
    # print(animal)

    avg_animal = summary_stats(animals)
    print(avg_animal)

if __name__ == '__main__':
    main()
