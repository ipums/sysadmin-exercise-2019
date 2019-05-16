# Intended to go in a MySQL docker image /docker-entrypoint-initdb.d/ dir,
# where the MySQL docker image infrastructure will run it after spinning
# up a container and bringing up the database.
# See https://hub.docker.com/_/mysql#initializing-a-fresh-instance

# Create persons table.
mysql -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < /ipums/schema.sql

# Populate persons table from census data extract.
mysql -u root -p$MYSQL_ROOT_PASSWORD --local-infile $MYSQL_DATABASE < /ipums/load.sql

