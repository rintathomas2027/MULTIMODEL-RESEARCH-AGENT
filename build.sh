#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "=========================================="
echo " Starting ScholarPulse Render Build..."
echo "=========================================="

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python -m pip install -r requirements.txt

# Collect static files with whitenoise
python manage.py collectstatic --noinput

# Run migrations safely (increments schema without data loss)
python manage.py migrate --noinput

# If data_dump.json exists and database is fresh, load data
if [ -f "data_dump.json" ]; then
    echo "Checking if database records need restoration..."
    python -c "
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_assistant.settings')
django.setup()
from assistant.models import Document
from django.core.management import call_command
if Document.objects.count() == 0:
    print('Importing existing documents and users from data_dump.json...')
    call_command('loaddata', 'data_dump.json')
    print('Restoration complete!')
else:
    print(f'Database already contains {Document.objects.count()} documents. Preserving data untouched.')
" || echo "Data check completed."
fi

echo "=========================================="
echo " ScholarPulse Build Completed Successfully!"
echo "=========================================="
