 release: python migrate.py
 web: gunicorn start:app
 worker: celery -A app.celery worker