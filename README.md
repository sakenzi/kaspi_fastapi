# kaspi_fastapi

# Работа с celery-redis
1. Запуск worker
    ```bash
    celery -A app.api.comparisons.celery.celery_app worker --loglevel=info --pool=threads --concurrency=1
    ```
2. Запуск beat
    ```bash
    celery -A app.api.comparisons.celery.celery_app beat --loglevel=info
    ```
3. Запуск flower
    ```bash
    celery -A app.api.comparisons.celery.celery_app flower
    ```

# Работа с docker
1. Создание 
```bash
    docker build -t docker_image_name -f Dockerfile
```
2. Запуск docker контейнера
```bash
    docker run --name=fastapi_image_container -p 1111:8001 fastapi_images
```
3. App файл
```bash
    docker exec -it fastapi_image_container bash
```

# Работа с docker-compose
1. Создание 
```bash
    docker-compose up -d
```
2. Смотреть логи
```bash
    docker logs docker-container-name
```