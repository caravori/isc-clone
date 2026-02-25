#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Only run migrations if needed (check if migrations table exists)
echo "Checking migrations..."
if python manage.py showmigrations 2>&1 | grep -q "\[ \]"; then
  echo "Running migrations..."
  python manage.py migrate --noinput
else
  echo "Migrations up to date"
fi

# Only collect static files if directory is empty
if [ ! -d "/app/staticfiles/admin" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput --clear
else
  echo "Static files already collected"
fi

echo "Starting application..."
exec "$@"
