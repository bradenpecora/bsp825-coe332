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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')