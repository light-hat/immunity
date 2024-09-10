#!/bin/sh

echo "DB not yet run..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

echo "DB did run."

python3 manage.py makemigrations --noinput

python3 manage.py migrate --noinput

python3 manage.py init_userspace

#python3 manage.py runserver 0.0.0.0:8000
gunicorn --bind 0.0.0.0:8000 core.wsgi:application
