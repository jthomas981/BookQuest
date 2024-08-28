#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py makemigrations background_task
python manage.py migrate

# Start the background task processor
# Ensure that the background task processor runs in the background
python manage.py process_tasks &
