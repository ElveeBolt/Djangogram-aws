#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

DJANGO_SUPERUSER_PASSWORD=$SUPERUSER_PASSWORD python manage.py createsuperuser --username $SUPERUSER_NAME --email $SUPERUSER_EMAIL --noinput

exec "$@"