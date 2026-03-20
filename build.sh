#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Auto-create superuser from env vars (safe to re-run — won't fail if user exists)
python manage.py createsuperuser --noinput || true
