from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "portrait_upscaler",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_track_started=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True
)