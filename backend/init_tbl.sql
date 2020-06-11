drop table if exists weather_param;
create table weather_param (
    record_id serial PRIMARY KEY,
    temperature real,
    humidity real,
    pressure real,
    record_time timestamp
);
