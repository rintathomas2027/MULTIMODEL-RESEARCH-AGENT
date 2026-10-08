#!/bin/bash
echo "===> Creating staticfiles directory..."
mkdir -p staticfiles

echo "===> Installing dependencies..."
python3 -m pip install --break-system-packages -r requirements.txt || python3 -m pip install -r requirements.txt

echo "===> Collecting static files..."
python3 manage.py collectstatic --noinput --clear || true

echo "===> Build completed successfully!"
