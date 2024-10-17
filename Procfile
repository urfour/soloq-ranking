web: gunicorn -k eventlet -w 1 app:app
worker: celery -A app.celery worker --loglevel=info
beat: celery -A app.celery beat --loglevel=info