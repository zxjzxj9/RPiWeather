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

create table weather_request (
    request_id serial primary key,
    request_time timestamp,
    coord_lon real,
    coord_lat real,
    weather_id real,
    weather_main text,
    weather_description text,
    weather_icon text,
    base text,
    main_temp real,
    main_feels_like real,
    main_temp_min real,
    main_temp_max real,
    main_pressure real,
    main_humidity real,
    visibility real,
    wind_speed real,
    wind_deg real,
    clouds_all real,
    dt int,
    sys_type int,
    sys_id int,
    sys_country text,
    sys_sunrise int,
    sys_sunset int,
    timezone int,
    id int,
    "name" int,
    cod int
);