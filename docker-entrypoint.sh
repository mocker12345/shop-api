python /code/manage.py db init
python /code/manage.py db upgrade
/usr/local/bin/gunicorn -w 4 -b :8000 wsgi:application