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
#

The flask and redis services can be containered using docker-compose. To build and run the image, execute the following from the `homework_midterm` directory:

```bash
[homework_midterm]$ docker-compose -p <name> up -d
```
- The `-p` flag is the project tag: change `<name>` to whatever you wish.
- The `-d` flag runs the container in daemon/detached mode. This flag is optional.

NOTE: The docker-compose has the redis service run under my user ID. To change this, replace the numbers in line 17 of `docker-compose.yml` with `"<your user id>:<your group id>"`.

## Usage

#### Generation:

Now that the application is up and running, animals must be put into the database. Animals can be generated with:

```bash
[homework_midterm]$ python3 generate_animals.py
```
#### Routes:

A variety of routes can be hit to interact with the animal data:

#

```bash
curl 'localhost:5026/animals'
```
Prints the list of all animals in the redis database.

#

```bash
curl 'localhost:5026/animals/delete_all'
```
Deletes all animals currently in the redis database.

#

```bash
curl 'localhost:5026/animals/uid?uid=<uid>'
```
Replace `<uid>` with an animal's UID to have the app return that animal.

#

```bash
curl 'localhost:5026/animals/edit?uid=<uid>&<stat_name1>=<stat_value1>&<state_name2>=<stat_value2>'
```
This route allows the user to edit a specific animal by passing its UID. Replace `<stat_name>` with any of the following: `head`,`body`,`legs`, or `tail`. Replace `<stat_value>` with the value you want to update for the specific statistic. Multiple stats can be adjusted at once with a single route. Simply add statistics and their value by appending `&<next_stat_name>=<next_stat_value>` to the route.

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
curl 'localhost:5026/animals/legs/average'
```
Prints the average number of legs per animal in the database.

#

```bash
curl 'localhost:5026/animals/total_count
```
Prints the total count of animals in the redis database.

## Removal

To take down the container:
```bash
[homework_midterm]$ docker-compose -p <name> down
```

To remove the image, first find the image ID with `docker images` (`grep` will help). Then:
```bash
[homework_midterm]$ docker rmi <image-id>
```

The database data is maintained in the file `/redis/datum/dump.rdb`. This file should be removed if the user does not wish to maintain the data.