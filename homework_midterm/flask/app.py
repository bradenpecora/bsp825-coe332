import json
from flask import Flask, jsonify, request
from datetime import datetime
import redis

app = Flask(__name__)

rd = redis.StrictRedis(host='redis', port=6379, db=0)

@app.route('/animals/load')
def load_file():
    """
    Loads file into redis database
    """
    with open("mydata/data_file.json", "r") as json_file:
        data = json.load(json_file)

    rd.set('animals_key', json.dumps(data))
    return "Animals loaded \n"

@app.route('/helloworld', methods=['GET'])
def hello_world():
    return "Hello World!!\n"

def get_data():
    """
    Gets data from "data_file.json"
    """
    # with open("data_file.json", "r") as json_file:
    #     userdata = json.load(json_file)
    data = rd.get('animals_key')
    if data is None: 
        # Everytime data is 'gotten', checks to see if data exists.
        # If data DNE, it is loaded from the .json file.
        load_file()
        data = rd.get('animals_key')
        print("No animals detected in database. Animals loaded from file")
    return json.loads(data)

@app.route('/animals', methods=['GET'])
def get_animals():
    """
    Returns a JSON formatted string containing a list of animals (in a dictionary).
    """
    return jsonify(get_data())

@app.route('/animals/head/<head_type>', methods=['GET'])
def get_animal_heads(head_type):
    """
    Returns a JSON formatted string containing a list of animals (in a dictionary) with the inputted head type.
    """
    animals = get_data()["animals"]
    print(type(animals))
    output = [animal for animal in animals if animal['head'] == head_type]
    return jsonify(output)

@app.route('/animals/legs/<n_legs>', methods=['GET'])
def get_animal_legs(n_legs):
    """
    Returns a JSON formatted string containing a list of animals (in a dictionary) with the inputted amount of legs.
    """
    animals = get_data()["animals"]
    print(type(animals))
    output = [animal for animal in animals if animal['legs'] == int(n_legs)]
    return jsonify(output)

#query a range of dates
@app.route('/animals/date_range', methods=['GET'])
def date_range():
    """"
    Returns all animals between the queried date range 'date1' and 'date2'. Date format is YYYY-MM-DD+HH:MM:SS.SSSSSS.
    """
    animals = get_data()["animals"]

    date1str = request.args.get('date1')
    date1 = datetime.strptime(date1str, "%Y-%m-%d %H:%M:%S.%f")

    date2str = request.args.get('date2')
    date2 = datetime.strptime(date2str, "%Y-%m-%d %H:%M:%S.%f")

    if date2 < date1:
        # swaps date1 and date2 if date2 < date1
        dummy_date = date1
        date1 = date2
        date2 = dummy_date

    output = []

    for animal in animals:
        animal_date = datetime.strptime(animal['created_on'], "%Y-%m-%d %H:%M:%S.%f")
        if animal_date >= date1 and animal_date <= date2:
            output.append(animal)

    return jsonify(output)

#selects a particular creature by its unique identifier
@app.route('/animals/uid', methods=['GET'])
def get_from_uid():
    """
    Returns the animal with the queried UID
    """
    animals = get_data()["animals"]
    print(type(animals))

    uid = request.args.get('uid')
    uid_found = False

    for animal in animals:
        if animal['uid'] == uid:
            output = animal
            uid_found = True
            break
    
    if uid_found:
        return jsonify(output)
    else:
        return "Animal not found \n"

#edits a particular creature by passing the UUID, and updated "stats"
@app.route('/animals/edit', methods=['GET'])
def edit_animal():
    """
    Edits the animal with the quiered UID. Adjusted quiered stat_name(s) with quiered stat_value(s)
    """
    animals = get_data()["animals"]
    uid = request.args.get('uid')

    #find animal index matching uid
    for animal in animals:
        if animal['uid'] == uid:
            for stat_name in ['head', 'body', 'arms', 'legs', 'tail']:
                stat_value = str(request.args.get(stat_name))
                if stat_value != 'None':
                    if stat_name == 'arms' or stat_name == 'legs' or stat_name == 'tail':
                        stat_value = int(stat_value)
                    animal[stat_name] = stat_value

    animal_dict = {'animals':animals}
    # with open('data_file.json', 'w') as f:
    #     json.dump(animal_dict, f, indent=2)
    rd.set('animals_key', json.dumps(animal_dict))
    return "Animal updated \n"

#deletes a selection of animals by a date range
@app.route('/animals/date_range/delete', methods=['GET'])
def delete_date_range():
    """"
    Deletes all animals between the queried date range 'date1' and 'date2'. Date format is YYYY-MM-DD+HH:MM:SS.SSSSSS.
    """
    animals = get_data()["animals"]

    date1str = request.args.get('date1')
    date1 = datetime.strptime(date1str, "%Y-%m-%d %H:%M:%S.%f")

    date2str = request.args.get('date2')
    date2 = datetime.strptime(date2str, "%Y-%m-%d %H:%M:%S.%f")

    if date2 < date1:
        # swaps date1 and date2 if date2 < date1
        dummy_date = date1
        date1 = date2
        date2 = dummy_date

    output = []

    for animal in animals:
        animal_date = datetime.strptime(animal['created_on'], "%Y-%m-%d %H:%M:%S.%f")
        if animal_date < date1 or animal_date > date2:
            output.append(animal)

    animal_dict = {'animals':output}
    # with open('data_file.json', 'w') as f:
    #     json.dump(animal_dict, f, indent=2)
    rd.set('animals_key', json.dumps(animal_dict))
    return "Animals removed \n"

#returns the average number of legs per animals
@app.route('/animals/legs/average', methods=['GET'])
def average_legs():
    """"
    Returns the average number of legs per animal of the animals in the redis database
    """
    animals = get_data()["animals"]
    print(type(animals))

    average = 0

    for animal in animals:
        average = average + animal['legs']
    
    average = average / len(animals)

    return jsonify(average)

#returns a total count of animals
@app.route('/animals/total_count', methods=['GET'])
def get_total_animal_count():
    """
    Returns the total count of animals in the redis database
    """
    animals = get_data()["animals"]
    print(type(animals))
    output = len(animals)
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')