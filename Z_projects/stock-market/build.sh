#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Running build.sh...."
echo "Installing requirements...."
pip install -r requirements.txt

echo "Running collectstatic...."
python manage.py collectstatic

echo "Running migrations...."
python manage.py migrate