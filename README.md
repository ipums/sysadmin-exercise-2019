# sysadmin-exercise-2019

These materials are used by candidates for hiring exercises for ISRDI IT positions.

Here is [Dean Peterson's]http://dean-e-peterson.github.io solution.

## Requirements
* A clone of this GitHub repository.
* docker
* docker-compose

## Instructions
1. Clone repository
1. `cd sysadmin-exercise-2019`
1. `docker-compose up -d`
This will do the following:
    1. Build a sysadmin-db image.
        1. Pull a mysql image from Docker Hub.
        1. Customize it.
    1. Build a sysadmin-app image.
        1. Pull a phusion/passenger-customizable image from Docker Hub.
        3. Customize it.
1. Wait a few seconds for the database to spin up and to allow the data to import.  Optionally watch progress with
`docker logs sysadmin-exercise-2019_sysadmin-db_1`
1. Browse to http://localhost:8080/ and try out app.
1. To stop do
`docker-compose down -v`
from the same directory (the directory with the docker-compose.yml file.)


