import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/helloworld', methods=['GET'])
def hello_world():
    return "Hello World!!\n"

def get_data():
    """
    Gets data from "data_file.json"
    """
    with open("data_file.json", "r") as json_file:
        userdata = json.load(json_file)
        return userdata

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
    animal_dict = get_data()
    animal_head_dict = {}
    animal_head_dict['animals'] = []
    
    for animal in animal_dict['animals']:
        if animal['head'] == head_type:
            animal_head_dict['animals'].append(animal)

    return jsonify(animal_head_dict)

@app.route('/animals/legs/<n_legs>', methods=['GET'])
def get_animal_legs(n_legs):
    """
    Returns a JSON formatted string containing a list of animals (in a dictionary) with the inputted amount of legs.
    """
    n_legs = int(n_legs)
    animal_dict = get_data()
    animal_head_dict = {}
    animal_head_dict['animals'] = []
    
    for animal in animal_dict['animals']:
        if animal['legs'] == n_legs:
            animal_head_dict['animals'].append(animal)

    return jsonify(animal_head_dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')