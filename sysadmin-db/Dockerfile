# Recommend tagging in docker build with -t sysadmin-db.
# Whatever the case, the ultimate hostname on an internal network
# should be sysadmin-db for the app layer to connect.

FROM mysql:8.0

# Set root password, and also tell the MySQL docker image
# to create an ipums databases with an ipums user when a
# container is brought up.
ENV MYSQL_ROOT_PASSWORD="CensusDataRGr8" \
    MYSQL_USER="ipums" \
    MYSQL_PASSWORD="sysadmin-exercise" \
    MYSQL_DATABASE="ipums"

# Copy items to populate database with.
WORKDIR /ipums/
COPY . .

# Extract required fields into format more easily imported into MySQL.
# Note: This could be done outside of image building before copying
# info into the image, but done here to reduce dependencies on the
# environment outside of Docker.
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3-minimal \
 && ./ExerciseExtract.py us1850a_combined.dat us1850a_extracted.csv \
 && apt-get purge -y --auto-remove python3-minimal

# Clean up.
RUN apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Place populate.sh script where the MySQL image stuff will call it
# NOT when building this image but AFTER spinning up a container
# from this image and starting the database.
RUN cp populate.sh /docker-entrypoint-initdb.d/ 

# Document the MySQL port that gets exposed.
EXPOSE 3306/tcp

