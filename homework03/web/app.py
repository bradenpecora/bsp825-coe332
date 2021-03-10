import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/helloworld', methods=['GET'])
def hello_world():
    return "Hello World!!\n"

def get_data():
    with open("data_file.json", "r") as json_file:
        userdata = json.load(json_file)
        return userdata

@app.route('/animals', methods=['GET'])
def get_animals():
    """
    Returns a json dump (string) that contains all of the data in the
    data_file.json file.
    """
    return json.dumps(get_data())

@app.route('/animals/head/<head_type>', methods=['GET'])
def get_animal_heads(head_type):
    """
    Returns a dictonary containing a list of animals with the inputted head type.
    """
    animal_dict = get_data()
    animal_head_dict = {}
    animal_head_dict['animals'] = []
    
    for animal in animal_dict['animals']:
        if animal['head'] == head_type:
            animal_head_dict['animals'].append(animal)

    return animal_head_dict

@app.route('/animals/legs/<n_legs>', methods=['GET'])
def get_animal_legs(n_legs):
    """
    Returns a dictonary containing a list of animals with the inputted amount of legs.
    """
    n_legs = int(n_legs)
    animal_dict = get_data()
    animal_head_dict = {}
    animal_head_dict['animals'] = []
    
    for animal in animal_dict['animals']:
        if animal['legs'] == n_legs:
            animal_head_dict['animals'].append(animal)

    return animal_head_dict

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')