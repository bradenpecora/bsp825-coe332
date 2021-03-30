# Homework: Midterm

In this homework, I have created a python script that generates random animals and a Docker container that stores the animals in a redis database and allows a user to interact with the animal database through flask.

## Dependencies

To run `generate_animals.py`, [python3.6](https://www.python.org/) or later is required. Furthermore, the `petname` library is required:

```bash
pip3 install --user petname
```

[Docker](https://www.docker.com/) and Docker-compose are required. All other dependencies are handeled by building the docker image.

cURL, or an alternative, is required to interact with the database.

## Installation

The files can be downloaded using git:

```bash
git clone https://github.com/bradenpecora/bsp825-coe332.git
```
The project can be found within the `homework_midterm` directory:

```bash
cd bsp825-coe332/homework_midterm
```
There are two ways to input data into the redis database. The fist of which invloves running the python script `generate_animals_json.py` This python script creates a JSON file in `/flask/mydata` called `data_file.json` containing a variety of random "animals". This file will be included in the Docker container. From the `homework_midterm` directory:

```bash
python3 generate_animals_json.py
```

Inputting the data to redis in the form of the .json file allows the data to be reloaded if the user wishes. However, the python script must be run BEFORE the container image is built. Alternatively, the user can use `generate_animals_redis.py` to send a new set of random animals to the redis database AFTER the image is built and the container is running.

```bash
python3 generate_animals_redis.py
```

#

The flask and redis services can be containered using docker-compose. To build and run the image, execute the following from the `homework_midterm` directory:

```bash
docker-compose -p <name> up -d
```
- The `-p` flag is the project tag: change `<name>` to whatever you wish.
- The `-d` flag runs the container in daemon/detached mode. This flag is optional.

NOTE: The docker-compose has the redis service run under my user ID. To change this, replace the numbers in line 17 of `docker-compose.yml` with `"<your user id>:<your group id>"`.

## Usage

Now that the application is up and running, a variety of routes can be hit to interact with the animal data:

```bash
curl 'localhost:5026/animals/load'
```
This route loads reloads the animals from `data_file.json` into the redis database, which would only be the case if `generate_animals_json.py` was run before building the image. Hitting this route without using `generate_animals_json.py` *will* result in an error!

#

```bash
curl 'localhost:5026/animals'
```
Prints the list of all animals in the redis database.

#

```bash
curl 'localhost:5026/animals/total_count'
```
Prints the total amount of animals currently in the redis database.

#

```bash
curl 'localhost:5026/animals/head/<head_type>'
```
Prints all animals with `<head_type>`.

#

```bash
curl 'localhost:5026/animals/legs/<n_legs>'
```
Prints all animals that have `<n_legs>`.

#

```bash
curl 'localhost:5026/animals/legs/average'
```
Prints the average number of legs per animal in the database.

#

```bash
curl 'localhost:5026/animals/date_range?date1=YYYY-MM-DD+HH:MM:SS.SSSSSS&date2=YYYY-MM-DD+HH:MM:SS.SSSSSS'
```
Prints all animals that were created on or within date1 and date2. Please note the format of the date. For example, March 28 2021 at 15 hours, 31 minutes, and 26.000000 seconds would be inputted as `2021-03-28+15:31:26.000000`. 

#

```bash
curl 'localhost:5026/animals/date_range/delete?date1=YYYY-MM-DD+HH:MM:SS.SSSSSS&date2=YYYY-MM-DD+HH:MM:SS.SSSSSS'
```
Following as before, this route will delete all animals on or between date1 and date2. Please see the above route for formatting.

#

```bash
curl 'localhost:5026/animals/uid?uid=<uid>'
```
Replace `<uid>` with an animal's UID to have the app return that animal.

#

```bash
curl 'localhost:5026/animals/edit?uid=<uid>&<stat_name1>=<stat_value1>&<state_name2>=<stat_value2>
```
This route allows the user to edit a specific animal by passing its UID. Replace `<stat_name>` with any of the following: `head`,`body`,`legs`, or `tail`. Replace `<stat_value>` with the value you want to update for the specific statistic. Multiple stats can be adjusted at once with a single route. Simply add statistics and their value by appending `&<next_stat_name>=<next_stat_value>` to the route.

## Removal

To take down the container:
```bash
docker-compose -p <name> down
```

To remove the image, first find the image ID with `docker images` (`grep` will help). Then:
```bash
docker rmi <image-id>
```