#!/bin/bash

python manage.py migrate
# python manage.py sass static/scss/main.scss static/css/main.css
python manage.py collectstatic --noinput

exec "$@"