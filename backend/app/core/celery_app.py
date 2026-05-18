from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "dclaw",
    broker=settings.redis_url,
    backend=settings.celery_result_backend or settings.redis_url,
)

celery_app.conf.update(
    task_serializer=settings.celery_task_serializer,
    accept_content=settings.celery_accept_content,
    result_expires=3600 * 24 * 7,
    task_track_started=True,
    task_time_limit=3600 * 4,
    worker_prefetch_multiplier=1,
)
