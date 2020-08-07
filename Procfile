release: python manage.py migrate --noinput
web: daphne ccticker.asgi:application --port $PORT --bind 0.0.0.0
worker: REMAP_SIGTERM=SIGQUIT celery worker --app ccticker.celery.app --loglevel info
worker: REMAP_SIGTERM=SIGQUIT celery --app ccticker.celery.app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler 
