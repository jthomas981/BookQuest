@echo off
REM Exit on error
setlocal enabledelayedexpansion
set errorlevel=0

REM Install dependencies
pip install -r requirements.txt || set errorlevel=1

REM Check for errors
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    exit /b %errorlevel%
)

REM Convert static asset files
python manage.py collectstatic --no-input || set errorlevel=1

REM Check for errors
if %errorlevel% neq 0 (
    echo Error: Failed to collect static files.
    exit /b %errorlevel%
)

REM Apply any outstanding database migrations
python manage.py migrate || set errorlevel=1

REM Check for errors
if %errorlevel% neq 0 (
    echo Error: Failed to apply migrations.
    exit /b %errorlevel%
)

echo Build completed successfully!
