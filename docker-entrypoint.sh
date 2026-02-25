#!/bin/bash

set -e

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL started"

# Give PostgreSQL a moment to fully initialize
sleep 2

echo "Creating migrations..."
python manage.py makemigrations --noinput || true

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Creating cache table..."
python manage.py createcachetable 2>/dev/null || true

echo "Starting application..."
exec "$@"
