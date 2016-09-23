#!/usr/bin/env bash
python /code/manage.py db init
python /code/manage.py db migrate
python /code/manage.py db upgrade
 /usr/local/bin/gunicorn -k gevent -b 0.0.0.0:8000 wsgi:application