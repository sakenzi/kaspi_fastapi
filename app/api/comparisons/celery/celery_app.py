
from celery import Celery
from celery.signals import worker_process_init, worker_ready
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

@worker_process_init.connect
def on_worker_process_init(**kwargs):
    logger.info("Сигнал worker_process_init сработал")
    try:
        from app.api.comparisons.celery.tasks import parse_kaspi_products
        task = parse_kaspi_products.delay()
        logger.info(f"Запущена задача parse_kaspi_products с ID: {task.id}")
    except Exception as e:
        logger.error(f"Ошибка при запуске parse_kaspi_products в worker_process_init: {str(e)}")

@worker_ready.connect
def on_worker_ready(**kwargs):
    logger.info("Сигнал worker_ready сработал")
    try:
        from app.api.comparisons.celery.tasks import parse_kaspi_products
        task = parse_kaspi_products.delay()
        logger.info(f"Запущена задача parse_kaspi_products с ID: {task.id}")
    except Exception as e:
        logger.error(f"Ошибка при запуске parse_kaspi_products в worker_ready: {str(e)}")

# if __name__ == "__main__":
#     celery.start()
