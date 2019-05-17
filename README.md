# sysadmin-exercise-2019

These materials are used by candidates for hiring exercises for ISRDI IT positions.

This forked repository contains Dean Peterson's solution.  

## Requirements
* A clone of this GitHub repository.
* docker
* docker-compose

## Instructions
1. Clone repository

2. `cd sysadmin-exercise-2019`

3. `docker-compose up -d`
This will build and spin up two images, a sysadmin-db image based on a docker hub MySQL image, and a sysadmin-app image based on a docker hub phusion/passenger-customizable image.

4. Wait a few seconds for the database to spin up and to allow the data to import.  Optionally watch progress with
`docker logs sysadmin-exercise-2019_sysadmin-db_1`

5. Browse to http://localhost:8080/ and try out app.

6. To stop do
`docker-compose down -v`
from the same directory (the directory with the docker-compose.yml file.)

## Implementation Notes

### sysadmin-db image

The sysadmin-db image build process extracts the relevant fields from the census data.  It also sets up environment variables and loading scripts that are used later during container spin up by stuff built in to the MySQL base image.  Database operations are deferred to this time to allow the MySQL base image to start up the database.

More specifically, the sysadmin-db image build process (see `sysadmin-db/Dockerfile`):
* Starts with [https://hub.docker.com/_/mysql](docker hub's MySQL image), specifically the latest MySQL 8 image.
* Sets some environment variables used by the MySQL image to set the root password and create an empty ipums database when spinning up the image later.  NOTE: Contains MySQL user names and passwords, so this is a security consideration.
* Copies files from `sysadmin-db` in this repository to a directory `/ipums/` inside the image.
* Briefly installs python 3 in order to run `sysadmin-db/ExerciseExtract.py`, which extracts the desired fields from the census data into a file that only lives on the image called `us1850a_extracted.csv`.  This means that the data is baked in to the image.  However, the CSV file is not loaded into the database until after a container is spun up from the image.  Since python is not needed on the database layer at runtime, it is immediately uninstalled. 
* Copies `sysadmin-db/populate.sh` into `/docker-entrypoint-initdb.d/`, the location that the MySQL image searches for initialization scripts to run after a container is spun up and the database is started.

The sysadmin-db container spin-up process:
* Brings up the database (functionality from the MySQL image)
* Creates an ipums user and an empty ipums database (functionality from the MySQL image, but triggered by our setting environment variables `MYSQL_USER` and `MYSQL_DATABASE` in our `sysadmin-db/Dockerfile`)
* Looks for files in `/docker-entrypoint-initdb.d/` to run (functionality from the MySQL image), and finds our `sysadmin-db/populate.sh` script.
* populate.sh uses the ISRDI-provided `sysadmin-db/schema.sql` file to create a persons table.
* populate.sh uses the `sysadmin-db/load.sql` to do a local load data from the `us1850a_extracted.csv` file extracted using python during the image build process earlier.

### sysadmin-app image

The sysadmin-app image build process is comparatively simple because it doesn't involve the two-stage build and spin-up procedure of the MySQL-based image.  Specifically, the sysadmin-app image build process:
* Builds on a [https://hub.docker.com/r/phusion/passenger-customizable](customizable phusion passenger image).  The full image is avoided to avoid having unneeded Ruby, node.js, etc. present.
* Uses the phusion-provided `/pd_build/python.sh` script to install python.
* Patches the operating system at sysadmin-app image build time, as [https://github.com/phusion/passenger-docker#upgrading_os](recommended by Phusion).  This can take some time, of course.
* Installs python packages Flask and Flask-MySQLdb as specified in `sysadmin-app/requirements.txt`.   Again, some additional packages such as pip are temporarily installed to allow this operation, then immediately removed because they are not needed at runtime.  The mysql client library is not removed because it is needed at runtime.  (See comments in `sysadmin-app/Dockerfile`)
* Copies the ISRDI-provided web app and `sysadmin-app/webapp.conf` into place to enable serving content.

The sysadmin-app container spin-up process doesn't do much.  It:
* Spins up the container.
* Starts the web server, which has passenger configured, which serves the ISRDI web app.
* Does not wait for the database to be available.

### docker-compose service composition
The `docker-compose.yml` file does not specify a network (it is commented out).  This lets it make use of the default network, which provides the nice functionality of letting containers be accessed over the internal network by the designated service name.  This means that when `sysadmin-app/config.py` in the web app container points to MYSQL_HOST = 'sysadmin-db', it can find the database container at that name because sysadmin-db is the service name given to it in `docker-compose.yml`.

Port 80 inside the web app server is exposed on the docker host as port 8080, to avoid any other web server running on the docker host.  This would probably be changed in production.


## Changes I made to ISRDI-provided materials
* Moved many items to `sysadmin-db` and `sysadmin-app` subdirectories.  This was partly organizational, and partly due to wanting to restrict the size of the docker path context which [https://docs.docker.com/engine/reference/commandline/build/#build-with-path](apparently) gets sent to the docker daemon in it entirety regardless of how much of the directory is actually referred to by the Dockerfile?
* Added a line to `sysadmin-app/webapp.conf` to specify using python 3 `passenger python /usr/bin/python3;`
* Used Flask-MySQLdb as specified in `sysadmin-app/app.py` instead of Flask-MySQL as mentioned in PDF instructions.

## Potential Improvements
Here are some things that could still be improved about this solution.
* MySQL user names and passwords could be moved to an env_file, or otherwise made more secure.  Also, using a random mysql root password could be explored.
* If ISRDI wanted to maintain the single-level directory structure, I could explore using a [https://docs.docker.com/engine/reference/commandline/build/#use-a-dockerignore-file](.dockerignore) file instead of subdirectories to restrict the amount of context sent to the docker daemon (assuming I am interpreting that issue correctly.)
* If python 3 was always available on the docker host doing the sysadmin-db image building, `sysadmin-db/ExerciseExtract.py` could be run on the docker host, and only the extracted fields would ever need to be added to the image, instead of doing that processing as part of the build process.  I did not do that to minimize external dependencies.

