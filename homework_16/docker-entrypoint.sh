#!/bin/sh
set -e

echo "Run migrations..."
python manage.py migrate

echo "Collect static..."
python manage.py collectstatic --noinput

echo "Start Django..."
python manage.py runserver 0.0.0.0:8000