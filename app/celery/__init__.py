import os
from celery import Celery


celery_app = Celery(
    "poetry_tasks",
    broker=os.environ["CELERY_BROKER_URL"],
    backend=os.environ["CELERY_RESULT_BACKEND"],
)

celery_app.conf.task_routes = {
    "app.celery.tasks.generate_poetry_task": {"queue": "poetry_queue"},
    "app.celery.tasks.generate_quote_task": {"queue": "poetry_queue"},
    "app.celery.tasks.generate_new_poem_task": {"queue": "poetry_queue"},
}

from app.celery import tasks