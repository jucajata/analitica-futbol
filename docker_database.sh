#!/bin/bash

# Pull the latest Postgres image
docker pull postgres

# Start a new container and set a password for the default "postgres" user
docker run --name postgres-af -e POSTGRES_PASSWORD=password -e TZ=America/Bogota -d -p 5441:5432 postgres

echo 'container created'
sleep 5

# Connect to the running container and create a database
docker exec -it postgres-af sh -c 'createdb dbaf -U postgres'

# Copy sql file for create tables
#docker cp create_tables.sql postgres-af:/home

# Create tables
#docker exec -it postgres-af psql -U postgres -d mydb -a -f /home/create_tables.sql