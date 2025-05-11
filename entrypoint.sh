#!/bin/bash

set -e

# Ensure correct permissions for SQLite database
touch /app/db.sqlite3
chmod 666 /app/db.sqlite3

# Generate migrations if needed
python manage.py makemigrations --noinput

# Apply database migrations
python manage.py migrate --noinput

# Run seed command
python manage.py seed || echo "Seed command skipped or failed"

# Start server (usando runserver pra testar)
python manage.py runserver 0.0.0.0:8000

