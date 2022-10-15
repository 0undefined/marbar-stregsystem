#!/usr/bin/env bash

# Creates DB tables and such
python3 manage.py makemigrations
python3 manage.py makemigrations cms
python3 manage.py migrate

# Copy static files to public directory
python3 manage.py collectstatic --no-input

# Run the bloody thing
python3 manage.py runserver 0.0.0.0:8000
