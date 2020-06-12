drop table if exists weather_param;
drop table if exists request_record;
create table weather_param (
    record_id serial primary key,
    temperature real,
    humidity real,
    pressure real,
    record_time timestamp
);
create table request_record (
    request_id serial primary key,
    request_time timestamp,
    record_id int references weather_param(record_id)
);
