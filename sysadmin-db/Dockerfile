# Recommend tagging in docker build with -t sysadmin-db.
# This is for consistency with the docker run --name which will give
# the resulting container instance the hostname it needs on internal
# networks for the app layer to connect to MYSQL_HOSTNAME=sysadmin-db.

FROM mysql:8.0

EXPOSE 3306/tcp

ENV \
    MYSQL_ROOT_PASSWORD="the" \
    MYSQL_USER="ipums" \
    MYSQL_PASSWORD="sysadmin-exercise" \
    MYSQL_DATABASE="ipums"

WORKDIR /ipums

COPY schema.sql .

# RUN mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -h127.0.0.1 -P3306  $MYSQL_DATABASE < /ipums/schema.sql
# RUN /bin/ps -efH
# RUN ['/bin/ps', '-efH']

