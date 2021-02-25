#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
docker-compose up --build
gunicorn bhavcopy.wsgi:application --bind 0.0.0.0:$PORT
redis-server
celery -A bhavcopy beat -l info
celery -A bhavcopy worker -l info

exec "$@"