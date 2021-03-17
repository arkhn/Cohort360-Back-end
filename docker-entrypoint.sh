#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Trace execution
[[ "${DEBUG}" ]] && set -x


export DJANGO_SETTINGS_MODULE=cohort_back.settings
export STATIC_ROOT="${FILES_ROOT}/static"

# Wait for db
sleep 5

if [[ "$#" -gt 0 ]]; then
  python django/manage.py "$@"
else
  echo "Apply database migrations"
  python manage.py makemigrations cohort
  python manage.py makemigrations explorations
  python manage.py migrate
  # Skip static files collection (not used)
  # python manage.py collectstatic --no-input
  if [[ "${ENV}" == "dev" ]]; then
    echo "Starting server"
    python manage.py runserver 0.0.0.0:8000
  else
    export UWSGI_PROCESSES=${UWSGI_PROCESSES:-5}
    export UWSGI_THREADS=${UWSGI_THREADS:-4}
    echo "Starting server"
    python manage.py check --deploy
    uwsgi --ini uwsgi.ini
  fi
fi