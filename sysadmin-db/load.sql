-- Load the extracted census data.
-- In addition to the SERVER-side local_infile setting below,
-- this requires logging on with mysql as root, and
-- passing --local-infile on the mysql CLIENT command line.

set global local_infile = true;

load data
    local
    infile 'us1850a_extracted.csv'
    into table persons
    -- character set utf8
    fields terminated by ',' optionally enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    ( unique_id,
      age,
      sex,
      race 
     );

set global local_infile = false;

-- select count(*) from persons;

