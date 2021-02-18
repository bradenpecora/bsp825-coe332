# Homework02: The Containers and Repositories of Dr. Moreau

This directory contains the second homework for COE332. This assignment is an extension of the first homwork, which could generate and parse .json files containing animal statistics. This homwork adds the `summary_stats` function to ['read_animals.py'](https://github.com/bradenpecora/bsp825-coe332/blob/main/homework02/read_animals.py), which prints average values for certain animal statistics. A [unit test](https://github.com/bradenpecora/bsp825-coe332/blob/main/homework02/test_read_animals.py) is included that can be ran on this function. Furthermore, the ability to containerize the project using
Docker was added in this assignment.

# Dependencies

To run the included scripts directly, [python3.6](https://www.python.org/) or later is required. Furthermore, the `petname` library is required:

```bash
pip3 install --user petname
```

[Docker](https://www.docker.com/) is required if the user wishes to containerize the assignment. 

# Installation

The files can be downloaded using git:

```bash
git clone https://github.com/bradenpecora/bsp825-coe332.git
```
The project can be found within the `homework02` directory:

```bash
cd bsp825-coe332/homework02
```

# Direct Usage

To run the scripts outside of a container, python3 is used from the command line. Navigate to the `homework02` directory within the repository.

First, animals must be generated. The following script generates `filename.json`, which contains statistics for 20 randomly generated animals:

```bash
python3 generate_animals.py filename.json
```

The generated file `filename.json` can be parsed by using the following script:

```bash
python3 read_animals.py filename.json
```

This script will print a random animal and the average statitics of the animals from the input file.

# Containerized Usage

If the user wishes to run the scripts from a container, an image can be assembled using the included [Dockerfile](https://github.com/bradenpecora/bsp825-coe332/blob/main/homework02/Dockerfile). To build the image, use:

```bash
docker build -t username/json-parser:1.0 .
```

Alternatively, the image can be pulled from DockerHub:

```bash
docker pull bradenpecora/json-parser:1.0
```
*The user can change 'username' accordingly, but, if the image is pulled, 'bradenpecora' must be used as the username.

To start a shell inside the image and run the scripts interactively:

```bash
docker run --rm -it username/json-parser:1.0 /bin/bash
```

The two scripts can be used from the shell within the image with the following:
```bash
generate_animals.py filename.json
read_animals.py filename.json
```

To exit the container, type `exit` on the command line.

The scripts within the image can also be ran non-interactively, outside of the container:
```bash
docker run --rm -v $PWD:/data -u $(id -u):$(id -g) username/json-parser:1.0 generate_animals.py /data/animals.json
docker run --rm -v $PWD:/data -u $(id -u):$(id -g) username/json-parser:1.0 read_animals.py /data/animals.json
```

These scripts can also be executed using docker-compose. Navigate to [`docker-compose.yaml`](https://github.com/bradenpecora/bsp825-coe332/blob/main/homework02/docker-compose.yaml) and change the user ID in line 10 to your own. The format is userID:groupID. Your user ID and group ID can be found using `id -u` and `id -g`, respectively, on the command line. To run the scripts, use the following on the command line:
```bash
docker-compose run gen-anim
docker-compose run read-anim
```
Running the files using docker-compose will create a json file called `animals.json` in /homework02/data

# Unit Test

To run the unit test on the `summary_stats` function in `read_animals.py`:

```bash
python3 test_read_animals.py
```
