#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Trace execution
[[ "${DEBUG}" ]] && set -x


export DJANGO_SETTINGS_MODULE=cohort_back.settings."${ENV:-prod}"
export STATIC_ROOT="${FILES_ROOT}/static"

if [[ "$#" -gt 0 ]]; then
  python manage.py "$@"
else
  python manage.py migrate
  # Skip static files collection (not used)
  # python manage.py collectstatic --no-input
  if [[ "${ENV}" == "dev" ]]; then
    python manage.py createsuperuser \
      --username "${DJANGO_SUPERUSER_USERNAME:-admin}" \
      --email "${DJANGO_SUPERUSER_EMAIL}" \
      --password "${DJANGO_SUPERUSER_PASSWORD}" \
      --no-input || echo "Skipping superuser creation."
    python manage.py runserver 0.0.0.0:8000
  else
    export UWSGI_PROCESSES=${UWSGI_PROCESSES:-5}
    export UWSGI_THREADS=${UWSGI_THREADS:-4}
    python manage.py check --deploy
    uwsgi --ini uwsgi.ini
  fi
fi