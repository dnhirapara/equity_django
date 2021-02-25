import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhavcopy.settings.dev")

app = Celery("bhavcopy")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
