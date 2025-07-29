#!/bin/sh

export DJANGO_SETTINGS_MODULE="config.$DJANGO_ENV"

if [ "$DJANGO_ENV" = "dev" ]; then
  export RELOAD="true"
fi

python3 manage.py makemigrations --no-input --settings=config.$DJANGO_ENV
python3 manage.py migrate --no-input --settings=config.$DJANGO_ENV
python3 manage.py collectstatic --no-input --settings=config.$DJANGO_ENV
python3 manage.py initdb --settings=config.$DJANGO_ENV


# if [ "$DJANGO_ENV" = "staging" ]; then
#   python3 manage.py ...
# fi

exec uvicorn config.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  ${RELOAD:+--reload}
