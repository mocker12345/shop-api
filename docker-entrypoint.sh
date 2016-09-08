python /code/manage.py db init
python /code/manage.py db migrate
python /code/manage.py db upgrade
/usr/local/bin/gunicorn -w 1 -b :8000 wsgi:application