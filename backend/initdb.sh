#! /bin/bash

createdb weather;
psql -d weather -f init_tbl.sql;
