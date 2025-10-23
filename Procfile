web: rm -rf staticfiles && python manage.py collectstatic --noinput && python manage.py migrate && gunicorn hashflix.wsgi --log-file -

