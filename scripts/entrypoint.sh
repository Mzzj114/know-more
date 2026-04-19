#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
# This gathers files from STATICFILES_DIRS (static/ and node_modules/) into STATIC_ROOT (staticfiles/)
python manage.py collectstatic --noinput

echo "Starting uWSGI..."
uwsgi --ini uwsgi.ini
