from .base import INSTALLED_APPS, MIDDLEWARE
from celery.schedules import crontab
import os
import bhavcopy.tasks
import pytz
from pytz import timezone

INSTALLED_APPS += [
    'rest_framework',
    'corsheaders',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')
# Redis

CACHE_TTL = 0
REDIS_URL = os.environ.get("REDIS_URL")
# REDIS_URL = "127.0.0.1"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://"+REDIS_URL+":6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "bhavcopy"
    }
}
REDIS_HOST = REDIS_URL
REDIS_PORT = 6379
# tasks.fetch_csv_task()


CELERY_BROKER_URL = "redis://"+REDIS_URL+":6379/2"
CELERY_RESULT_BACKEND = "redis://"+REDIS_URL+":6379/2"
CELERY_TIMEZONE = timezone('Asia/Kolkata')
CELERY_BEAT_SCHEDULE = {}
if int(os.environ.get("RUN_TASK", default=1)):
    CELERY_BEAT_SCHEDULE = {
        "fetch_csv_task": {
            "task": "bhavcopy.tasks.fetch_csv_task",
            # "schedule": crontab(minute='6', hour='18', day_of_week=[1, 2, 3, 4, 5]),
            "schedule": crontab(minute='*/1'),
        },
    }
else:
    CELERY_BEAT_SCHEDULE = {
        "fetch_csv_task": {
            "task": "bhavcopy.tasks.fetch_csv_task",
            "schedule": crontab(minute='2', hour='18', day_of_week=[1, 2, 3, 4, 5]),
            # "schedule": crontab(minute='*/1'),
        },
    }

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'CORS',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'X-Custom-Information',
]
