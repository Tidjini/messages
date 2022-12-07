#!/bin/bash

# installations
echo "building messages project"
python3.9 -m pip install -r requirements.txt
# todo later if needed echo "Pipenv setup"
echo "Run Migrations"
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput
echo "Collecting static files"
python3.9 manage.py collectstatic --noinput --clear
