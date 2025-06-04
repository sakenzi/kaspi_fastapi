from celery import Celery
# from celery.signals import worker_process_init
# from app.api.comparisons.celery.tasks import parse_kaspi_products

celery = Celery(
    "kaspi_parser",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.api.comparisons.celery.tasks"]
)

celery.conf.beat_schedule = {
    'parse-kaspi-products-every-2-hours': {
        'task': 'app.api.comparisons.celery.tasks.parse_kaspi_products',
        'schedule': 240.0,
    }
}

celery.conf.timezone = 'UTC'

# @worker_process_init
# def on_worket_init(**kwargs):
#     task = parse_kaspi_products.delay()

# if __name__ == "__main__":
#     celery.start()