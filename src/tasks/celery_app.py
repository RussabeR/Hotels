from celery import Celery

celery_ = Celery(
    'tasks',
)
