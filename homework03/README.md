# Homework 3: Flask

This directory contains the third homework for COE332. In this assignment, a Flask app was developed that can return (filtered) information from an ['included file'](https://github.com/bradenpecora/bsp825-coe332/blob/main/homework03/web/data_file.json)). This app can be run from the command line directly, or through a Docker container. Instructions for interacting with the app both ways are provided.

The ['app'](https://github.com/bradenpecora/bsp825-coe332/blob/main/homework03/web/app.py), ['data file'](https://github.com/bradenpecora/bsp825-coe332/blob/main/homework03/web/data_file.json), and files needed to containerize the app are in the ['/web'](https://github.com/bradenpecora/bsp825-coe332/blob/main/homework03/web) directory. The consumer file (['requestor.py'](https://github.com/bradenpecora/bsp825-coe332/blob/main/homework03/requestor.py)).

# Dependencies

To run the included scripts directly, [python3.6](https://www.python.org/) or later is required.

Flask is required to run the Flask app from the command line:

```bash
pip3 install --user flask
```

Curl or another alternative is required to interact with the Flask app from the command line.

[Docker](https://www.docker.com/) is required if the user wishes to containerize the assignment. 

# Installation

The files can be downloaded using git:

```bash
git clone https://github.com/bradenpecora/bsp825-coe332.git
```
The project can be found within the `homework03` directory:

```bash
cd bsp825-coe332/homework03
```

# Containerization

If the user wishes to build an image to containerize the app, this can be done by navigating to the `\web` directory and executing the following:

```bash
docker build -t <an-image-name>:latest .
docker run --name "give your container a name" -d -p <your portnumber>:5000 <an-image-name>
```

To stop the container, first find the container number with `docker ps -a`. Then execute `docker stop <container number>`.
To remove the container, execute `docker rmi <container number>`.

# Running App in Command Line

If the user wishes to run the Flask app from the command line, they can execute the following from `\web`:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run -h localhost -p <your_port>
```

# Using the App

Now that the app is running either in the command line or a container, the app can be interacted with. The app can do the following:

- Return all animals in `data_file.json`:
```bash
curl localhost:<port>/animals 
```
- Return all animals from `data_file.json` with a specific head type:
```bash
curl localhost:<port>/animals/head/<head_type>
```

- Return all animals from `data_file.json` with a specific amount of legs:
```bash
curl localhost:<port>/animals/legs/<number_of_legs>
```

Alternatively, the app can be interacted with by using the `requestor.py` python script. The user can change the URL accordingly to consume data from the app.