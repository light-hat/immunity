#!/bin/sh

export DJANGO_SETTINGS_MODULE="config.$DJANGO_ENV"

if [ "$DJANGO_ENV" = "dev" ]; then
  export RELOAD="true"
fi

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

if [ "$DJANGO_ENV" = "staging" ]; then
  python manage.py ...
fi

exec uvicorn config.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  ${RELOAD:+--reload}
