#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

python manage.py schemamigration background_task --init
# Run database migrations
python manage.py migrate 

# Start the background task processor
# Ensure that the background task processor runs in the background
python manage.py process_tasks &
