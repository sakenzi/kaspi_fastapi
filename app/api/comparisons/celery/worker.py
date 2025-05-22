from app.api.comparisons.celery.celery_app import celery


if __name__ == "__main__":
    celery.worker_main(["worker", "--loglevel=info", "--concurrency=1"])