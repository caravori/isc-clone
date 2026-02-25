#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
echo "Creating migrations..."
python manage.py makemigrations --noinput

echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Setup initial data (superuser, site, etc)
if [ "$SETUP_DB" = "true" ]; then
  echo "Setting up initial database..."
  /bin/sh /app/scripts/setup_db.sh
fi

echo "Starting application..."
exec "$@"
