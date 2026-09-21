#!/bin/sh
set -e

echo "Run migrations..."
python manage.py migrate

echo "Collect static..."
python manage.py collectstatic --noinput

echo "Start Django..."
exec gunicorn bookstore.wsgi:application --bind 0.0.0.0:8000
