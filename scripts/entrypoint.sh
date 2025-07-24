#!/bin/sh

if [ "$DJANGO_ENV" = "dev" ]; then
  RELOAD="true"
fi

if [ "$DJANGO_ENV" = "staging" ] || [ "$DJANGO_ENV" = "prod" ]; then
  python manage.py migrate --no-input
  python manage.py collectstatic --no-input
fi

if [ "$DJANGO_ENV" = "staging" ]; then
  python manage.py ...
fi

exec uvicorn config.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  ${RELOAD:+--reload}
