# Базовый слой для зависимостей
FROM python:3.12-slim AS base

# Устанавливаем зависимости для сборки и тестирования
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl

# Устанавливаем рабочую директорию
WORKDIR /home/app/web

COPY requirements.txt .

# Устанавливаем зависимости приложения
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все содержимое проекта в контейнер
COPY . .

ENV DJANGO_SETTINGS_MODULE=conf.settings.prod

# Старт управляющего сервера
FROM base AS server

# Назначаем права на исполнение
RUN chmod +x entrypoint.sh

# Запускаем скрипт инициализации
ENTRYPOINT ["sh", "./entrypoint.sh"]

# Старт асинхронного воркера
FROM base AS worker

# Указываем команду для запуска приложения
CMD ["celery", "-A", "conf", "worker", "--loglevel=info"]
