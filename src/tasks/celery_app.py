from celery import Celery
from celery.schedules import crontab
from src.config import settings

celery_instance = Celery(
    "tasks", broker=settings.REDIS_URL, include=["src.tasks.tasks"]
)

celery_instance.conf.beat_schedule = {
    "Рандомное название": {
        "task": "Booking_today_checkin",
        "schedule": crontab(hour=16, minute=48),
    },
}

celery_instance.conf.timezone = "Europe/Moscow"
