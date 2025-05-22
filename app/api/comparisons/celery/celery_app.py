from celery import Celery


celery = Celery(
    "kaspi_parser",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.api.comparisons.celery.tasks"]
)