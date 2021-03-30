import json
from flask import Flask, jsonify, request
from datetime import datetime
import redis

app = Flask(__name__)

rd = redis.StrictRedis(host='redis', port=6379, db=0)

@app.route('/helloworld', methods=['GET'])
def hello_world():
    return "Hello World!!\n"

@app.route('/animals', methods=['GET'])
def get_animals():
    """
    Returns all animals
    """
    animals = {}
    for key in rd.scan_iter():
        animals[key] = rd.hgetall(key)
    return jsonify(animals)

@app.route('/animals/delete_all', methods=['GET'])
def delete_all_animals():
    """
    Removes all animals from redis database
    """
    for key in rd.scan_iter():
        rd.delete(key)
    return "All animals deleted \n"

# query a range of dates
@app.route('/animals/date_range', methods=['GET'])
def date_range():
    """"
    Returns all animals between the queried date range 'date1' and 'date2'. Date format is YYYY-MM-DD+HH:MM:SS.SSSSSS.
    """
    date1str = request.args.get('date1')
    date1 = datetime.strptime(date1str, "%Y-%m-%d %H:%M:%S.%f")

    date2str = request.args.get('date2')
    date2 = datetime.strptime(date2str, "%Y-%m-%d %H:%M:%S.%f")

    if date2 < date1:
        # swaps date1 and date2 if date2 < date1
        # We need date1 < date2
        dummy_date = date1
        date1 = date2
        date2 = dummy_date

    output = {}

    for key in rd.scan_iter():
        animal_date = datetime.strptime(rd.hget(key,'created_on'), "%Y-%m-%d %H:%M:%S.%f")
        if animal_date >= date1 and animal_date <= date2:
            output[key] = rd.hgetall(key)

    return jsonify(output)

# selects a particular creature by its unique identifier
@app.route('/animals/uid', methods=['GET'])
def get_from_uid():
    """
    Returns the animal with the queried UID
    """
    uid = request.args.get('uid')
    return jsonify(rd.hgetall(uid))

#edits a particular creature by passing the UUID, and updated "stats"
@app.route('/animals/edit', methods=['GET'])
def edit_animal():
    """
    Edits the animal with the quiered UID. Adjusted quiered stat_name(s) with quiered stat_value(s)
    """
    uid = request.args.get('uid')

    for stat_name in ['head', 'body', 'arms', 'legs', 'tail']:
        stat_value = str(request.args.get(stat_name))
        if stat_value != 'None':
            rd.hset(uid, stat_name, stat_value)

    return jsonify(rd.hgetall(uid))

# deletes a selection of animals by a date range
@app.route('/animals/date_range/delete', methods=['GET'])
def delete_date_range():
    """"
    Deletes all animals between the queried date range 'date1' and 'date2'. Date format is YYYY-MM-DD+HH:MM:SS.SSSSSS.
    """
    date1str = request.args.get('date1')
    date1 = datetime.strptime(date1str, "%Y-%m-%d %H:%M:%S.%f")

    date2str = request.args.get('date2')
    date2 = datetime.strptime(date2str, "%Y-%m-%d %H:%M:%S.%f")

    if date2 < date1:
        # swaps date1 and date2 if date2 < date1
        # We need date1 < date2
        dummy_date = date1
        date1 = date2
        date2 = dummy_date

    for key in rd.scan_iter():
        animal_date = datetime.strptime(rd.hget(key,'created_on'), "%Y-%m-%d %H:%M:%S.%f")
        if animal_date >= date1 and animal_date <= date2:
            rd.delete(key)

    return "Animals Removed \n"

# returns the average number of legs per animals
@app.route('/animals/legs/average', methods=['GET'])
def average_legs():
    """"
    Returns the average number of legs per animal of the animals in the redis database
    """

    average = 0
    amount = 0

    for key in rd.scan_iter():
        legs = rd.hget(key, 'legs')
        if isinstance(legs, str):
            # Need legs to be a number
            legs = 0
        average = average + float(legs)
        amount = amount + 1
    
    if amount == 0:
        # Can't divide by zero
        amount = 1

    average = average / amount

    return jsonify(average)

# returns a total count of animals
@app.route('/animals/total_count', methods=['GET'])
def get_total_animal_count():
    """
    Returns the total count of animals in the redis database
    """
    amount = 0

    for key in rd.scan_iter():
        amount = amount + 1
    return jsonify(amount)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')