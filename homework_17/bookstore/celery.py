import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore.settings")

app = Celery("bookstore")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "generate-orders-report-every-day": {
        "task": "orders.tasks.generate_orders_report",
        "schedule": crontab(hour=9, minute=0),
    },
    "clear-expired-sessions-every-day": {
        "task": "orders.tasks.clear_expired_sessions",
        "schedule": crontab(hour=10, minute=0),
    },
}