#!/bin/sh

set -e

echo "Running migrations"
python3 manage.py makemigrations

python3 manage.py migrate

echo "Collecting Statics"
python3 manage.py collectstatic --noinput

