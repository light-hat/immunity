#!/bin/sh

echo "DB not yet run..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

echo "DB did run."

envsubst < /home/app/web/static/config.template.json > /home/app/web/static/config.json
exec "$@"

python3 manage.py makemigrations --noinput --settings=conf.settings.prod

python3 manage.py migrate --noinput --settings=conf.settings.prod

python3 manage.py init_users --settings=conf.settings.prod

gunicorn --bind 0.0.0.0:8000 conf.wsgi:application
