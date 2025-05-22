from app.api.comparisons.celery.celery_app import celery
from database.db import SessioLocal


@celery.task
def start_training_task(
    kaspi_email: str, 
    kaspi_password: str, 
    vender_code: str, 
    min_price: int,
    max_price: int,
    step: int
):
    db = SessioLocal()
    try: 
        print()
    finally:
        db.close()