#!/usr/bin/env python3
import json
import petname
import random
import sys
import uuid
import datetime
import redis

def main():

    rd = redis.StrictRedis(host='127.0.0.1', port=6406, db=0)

    for i in range(20):
        head = random.choice(['snake', 'bull', 'lion', 'raven', 'bunny'])
        body = petname.name() + '-' + petname.name()
        arms = random.randint(1,5) * 2
        legs = random.randint(1,4) * 3
        tail = legs + arms
        created_on = str(datetime.datetime.now())
        uid = str(uuid.uuid4())

        rd.hmset(uid, {'head' : head, 'body' : body, 'arms' : arms, 'legs' : legs, 'tail' : tail, 'created_on' : created_on})

if __name__ == '__main__':
    main()
